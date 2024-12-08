{inputs, ...}: {
  imports = [
    inputs.treefmt-nix.flakeModule
  ];
  perSystem = {
    config,
    pkgs,
    ...
  }: {
    treefmt.config = {
      projectRootFile = "flake.nix";
      package = pkgs.treefmt;
      programs = {
        ruff-check.enable = true;
        ruff-format.enable = true;

        prettier.enable = true;

        alejandra.enable = true;
        deadnix.enable = true;
        statix.enable = true;
      };
    };
  };
}
