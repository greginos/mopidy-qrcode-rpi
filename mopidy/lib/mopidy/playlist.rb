module Mopidy
  module Playlist
    def self.as_list
      json = Mopidy.format_json(1, 'core.playlists.as_list')
      Mopidy.post(json)
    end

    def self.lookup(uri)
      json = Mopidy.format_json(1, 'core.playlists.lookup', [uri])
      Mopidy.post(json)
    end

    def self.save(playlist)
      json = Mopidy.format_json(1, 'core.playlists.save', playlist: playlist)
      Mopidy.post(json)
    end
  end
end
