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
          help = "Run a dev environment of frontend";
          name = "front";
          command = "cd frontend && ${pkgs.nodejs}/bin/npm install && ${pkgs.nodejs}/bin/npm run dev";
        }
      ];
    };
  };
}
