# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'mopidy/version'

Gem::Specification.new do |spec|
  spec.name          = 'ruby-mopidy'
  spec.version       = Mopidy::VERSION
  spec.authors       = ['khisakuni', 'ares']
  spec.email         = ['kohei@gophilosophie.com', 'ares@igloonet.com']

  spec.summary       = 'A wrapper around the Mopidy API.'
  spec.homepage      = 'https://github.com/ares/mopidy'
  spec.license       = 'MIT'

  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  spec.bindir        = 'exe'
  spec.executables   = spec.files.grep(%r{^exe/}) { |f| File.basename(f) }
  spec.require_paths = ['lib']

  spec.add_dependency 'httparty'

  spec.add_development_dependency 'bundler'
  spec.add_development_dependency 'rake'
  spec.add_development_dependency 'rspec'
  spec.add_development_dependency 'pry'
end
