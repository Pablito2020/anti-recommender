{
  inputs,
  self,
  ...
}: {
  imports = [
    inputs.process-compose-flake.flakeModule
  ];
  perSystem = {system, ...}: {
    process-compose.default = {
      settings.processes = {
        backend-server.command = "${self.apps.${system}.backend.program}";
        frontend-server.command = "${self.apps.${system}.frontend.program}";
      };
    };
  };
}
