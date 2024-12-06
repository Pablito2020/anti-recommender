{
  inputs,
  self,
  ...
}: {
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
    packages.frontend = inputs.dream2nix.lib.evalModules {
      packageSets.nixpkgs = inputs.nixpkgs.legacyPackages.${system};
      modules = [
        derivation
        {
          inherit paths;
        }
      ];
    };
    packages.frontend-docker = pkgs.dockerTools.buildLayeredImage {
      name = "frontend-antirecommender";
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
    apps.frontend.program = program;
  };
}
