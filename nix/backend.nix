{inputs, ...}: {
  imports = [
    inputs.treefmt-nix.flakeModule
    inputs.pre-commit-hooks.flakeModule
  ];
  perSystem = {
    pkgs,
    config,
    ...
  }: let
    inherit (inputs.nixpkgs) lib;
    backendPath = ./../backend;
    # Python Env
    python = pkgs.python313;
    workspace = inputs.uv2nix.lib.workspace.loadWorkspace {workspaceRoot = backendPath;};
    overlay = workspace.mkPyprojectOverlay {
      sourcePreference = "wheel";
    };
    baseSet = pkgs.callPackage inputs.pyproject-nix.build.packages {
      inherit python;
    };
    pythonSet = baseSet.overrideScope (
      lib.composeManyExtensions [
        inputs.pyproject-build-systems.overlays.default
        overlay
      ]
    );
    venv = pythonSet.mkVirtualEnv "backend" workspace.deps.default;

    # mypy
    mypy = pkgs.writeShellScriptBin "mypy" ''
      "${venv}/bin/mypy"
    '';

    # ASGI app
    asgiServer = "${venv}/bin/uvicorn";
    asgiApp = "backend.main:app";
    options = pkgs.lib.cli.toGNUCommandLine {} {
      host = "0.0.0.0";
      port = 8000;
    };
    executeServerCommand = "${asgiServer} ${asgiApp} ${pkgs.lib.strings.concatStringsSep " " options}";
    start = pkgs.writeShellScriptBin "server" ''
      cd ${backendPath}
      ${executeServerCommand}
    '';
  in {
    # nix build .#backend generates a docker image
    packages.backend = pkgs.dockerTools.buildLayeredImage {
      name = "backend-antirecommender";
      tag = "latest";
      contents = [pkgs.cacert];
      config = {
        Cmd =
          [
            asgiServer
            asgiApp
          ]
          ++ options;
      };
    };
    # When we do nix run .#backend, execute the server
    apps.backend.program = "${pkgs.lib.getExe start}";

    # Linters, mypy checking, etc.
    treefmt.config.programs = {
      mypy = {
        enable = true;
        package = mypy;
        directories = {
          "backend".modules = [
            "src"
          ];
        };
      };
      ruff-check.enable = true;
      ruff-format.enable = true;
    };

    # Enable pre-commit hook of the treefmt declared before
    pre-commit = {
      settings = {
        hooks = {
          treefmt = {
            enable = true;
            pass_filenames = false;
          };
        };
      };
    };

    # Add this virtualenv inside the devshell, so we can access pyhton with the dependencies
    # we installed like it's just our "normal" python installation package
    devshells.default.packages = [venv];
  };
}
