{
  inputs,
  # self,
  ...
}: {
  perSystem = {
    system,
    ...
  }:
  {
    packages.frontend = inputs.dream2nix.lib.evalModules {
        packageSets.nixpkgs = inputs.nixpkgs.legacyPackages.${system};
        modules = [
          # Import our actual package definiton as a dream2nix module from ./default.nix
          ./frontend.nix
          {
            # Aid dream2nix to find the project root. This setup should also works for mono
            # repos. If you only have a single project, the defaults should be good enough.
            paths.projectRoot = ./.;
            # can be changed to ".git" or "flake.nix" to get rid of .project-root
            paths.projectRootFile = "flake.nix";
            paths.package = ./.;
          }
        ];
    };
  };
}
