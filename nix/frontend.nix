{
  inputs,
  self,
  ...
}: {
  imports = [
    inputs.treefmt-nix.flakeModule
    inputs.pre-commit-hooks.flakeModule
  ];
  perSystem = {
    system,
    pkgs,
    ...
  }: let
    paths = {
      projectRoot = ./..;
      projectRootFile = "flake.nix";
      package = ./..;
    };
    derivation = {
      config,
      dream2nix,
      ...
    }: {
      imports = [
        dream2nix.modules.dream2nix.nodejs-package-lock-v3
        dream2nix.modules.dream2nix.nodejs-granular-v3
      ];
      mkDerivation = {
        src = ./../frontend;
      };
      deps = {nixpkgs, ...}: {
        inherit
          (nixpkgs)
          fetchFromGitHub
          stdenv
          ;
      };
      nodejs-package-lock-v3 = {
        packageLockFile = "${config.mkDerivation.src}/package-lock.json";
      };
      name = "anti-recommender";
      version = "0.1.0";
    };
    staticFiles = "${self.packages.${system}.frontend}/lib/node_modules/anti-recommender/dist";
    server = pkgs.writeShellScriptBin "server-frontend" "${pkgs.caddy}/bin/caddy file-server --listen localhost:5173 --root ${staticFiles}";
    program = pkgs.lib.getExe server;
  in {
    # nix build .#frontend generates the static files
    packages.frontend = inputs.dream2nix.lib.evalModules {
      packageSets.nixpkgs = inputs.nixpkgs.legacyPackages.${system};
      modules = [
        derivation
        {
          inherit paths;
        }
      ];
    };

    # nix build .#frontend-docker builds a docker image with caddy
    packages.frontend-docker = pkgs.dockerTools.buildLayeredImage {
      name = "frontend-antirecommender";
      tag = "latest";
      config = {
        Cmd = [
          "${pkgs.caddy}/bin/caddy"
          "file-server"
          "--listen"
          "0.0.0.0:5173"
          "--root"
          staticFiles
        ];
      };
    };

    # Enable pre-commit hooks (eslint and prettier in treefmt)
    pre-commit = {
      check.enable = false; # We're working with the current directory path, gives an error when building on nix sandbox
      settings = {
        hooks = {
          eslint = {
            enable = true;
            pass_filenames = false;
            entry = "${self.packages.${system}.frontend}/lib/node_modules/.bin/eslint -c frontend/eslint.config.js frontend";
            settings.extensions = "\\.(js|ts|jsx|tsx|md|mdx|cjs|ts)$";
            verbose = true;
          };
          treefmt = {
            enable = true;
            pass_filenames = false;
          };
        };
      };
    };
    treefmt.config.programs.prettier.enable = true;

    # nix run .#frontend executes a dummy server with the static files generated
    apps.frontend.program = program;
  };
}
