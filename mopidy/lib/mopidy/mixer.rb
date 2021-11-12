module Mopidy
  module Mixer
    def self.volume
      json = Mopidy.format_json(1, 'core.mixer.get_volume')
      Mopidy.post(json)
    end

    def self.volume=(value)
      json = Mopidy.format_json(1, 'core.mixer.set_volume', [value])
      Mopidy.post(json)
    end
  end
end
