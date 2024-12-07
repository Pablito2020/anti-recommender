{inputs, ...}: {
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
  in {
    packages.backend = pkgs.dockerTools.buildLayeredImage {
      name = "backend-antirecommender";
      contents = [pkgs.cacert];
      config = {
        Cmd = [
          "${venv}/bin/uvicorn"
          asgiApp
        ];
      };
    };
    apps.backend.program = "${pkgs.lib.getExe start}";
  };
}
