{inputs, ...}: {
  imports = [
    inputs.pre-commit-hooks.flakeModule
  ];
  perSystem = _: {
    pre-commit = {
      settings = {
        hooks = {
          treefmt = {
            enable = true;
            pass_filenames = false; # Run it on all the files inside the repository
          };
          commitizen.enable = true;
        };
      };
    };
  };
}
