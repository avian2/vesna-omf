# -*- encoding: utf-8 -*-
require File.expand_path('../lib/omf_rc_logatec/version', __FILE__)

Gem::Specification.new do |gem|
	gem.authors       = ["Tomaz Solc"]
	gem.email         = ["tomaz.solc@ijs.si"]
	gem.description   = %q{OMF6 Resource Controller related to the Log-a-tec testbed}
	gem.summary       = %q{OMF6 Resource Controller related to the Log-a-tec testbed}
	gem.homepage      = "http://www.log-a-tec.eu"

	gem.files         = `git ls-files`.split($\)
	gem.name          = "omf_rc_logatec"
	gem.require_paths = ["lib"]
	gem.version       = OmfRcLogatec::VERSION
	gem.license       = "GPL"
	gem.add_runtime_dependency "omf_rc", "~> 6.1"
end
