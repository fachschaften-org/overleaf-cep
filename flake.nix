{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    systems.url = "github:nix-systems/default";
  };

  outputs = inputs: inputs.flake-parts.lib.mkFlake { inherit inputs; } {
    systems = import inputs.systems;
    perSystem = { pkgs, ... }: {

      devShells.default = pkgs.mkShellNoCC {
        packages = [
          pkgs.nodejs_26
          # for tools/logo
          (pkgs.python313.withPackages (python-pkgs: [
            python-pkgs.pyyaml
            python-pkgs.pillow
          ]))
          pkgs.icoutils
        ];
      };

    };
  };
}
