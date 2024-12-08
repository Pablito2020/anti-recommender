{inputs, ...}: {
  imports = [
    inputs.pre-commit-hooks.flakeModule
  ];
  perSystem = _: {
    pre-commit = {
      settings = {
        hooks = {
          commitizen.enable = true;
        };
      };
    };
  };
}
