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
        alejandra.enable = true;
        deadnix.enable = true;
        statix.enable = true;
        prettier.enable = true;
        mypy.enable = true;
        ruff-check.enable = true;
        ruff-format.enable = true;
      };
    };
    formatter = config.treefmt.build.wrapper;
  };
}
