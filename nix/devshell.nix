{inputs, ...}: {
  imports = [
    inputs.devshell.flakeModule
  ];
  perSystem = {
    config,
    pkgs,
    ...
  }: {
    devshells.default = {
      packages = [
        config.treefmt.build.wrapper
        pkgs.nodejs
        pkgs.git
        pkgs.git-crypt
        pkgs.python313
        pkgs.uv
      ];
      devshell.startup.pre-commit.text = config.pre-commit.installationScript;
      commands = [
        {
          help = "Get a dev environment up and running with everything you need!";
          name = "devenv";
          command = "nix run .";
        }
      ];
    };
  };
}
