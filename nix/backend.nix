{inputs, ...}: {
  imports = [
    inputs.treefmt-nix.flakeModule
    inputs.pre-commit-hooks.flakeModule
  ];
  perSystem = {pkgs, ...}: let
    inherit (inputs.nixpkgs) lib;
    backendPath = ./../backend;
    asgiApp = "backend.main:app";
    workspace = inputs.uv2nix.lib.workspace.loadWorkspace {workspaceRoot = backendPath;};
    overlay = workspace.mkPyprojectOverlay {
      sourcePreference = "wheel";
    };
    python = pkgs.python313;
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
    start = pkgs.writeShellScriptBin "server" ''
      cd ${backendPath}
      ${venv}/bin/uvicorn ${asgiApp}
    '';

    mypy = pkgs.writeShellScriptBin "mypy" ''
      "${venv}/bin/mypy"
    '';
  in {
    # nix build .#backend generates a docker image
    packages.backend = pkgs.dockerTools.buildLayeredImage {
      name = "backend-antirecommender";
      tag = "latest";
      contents = [pkgs.cacert];
      config = {
        Cmd = [
          "${venv}/bin/uvicorn"
          asgiApp
        ];
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
  };
}
