module Mopidy
  module Tracklist
    def self.load_playlist(playlist)
      clear
      playlist[:tracks].each do |track|
        add(track)
      end
    end

    def self.tracks
      json = Mopidy.format_json(1, 'core.tracklist.get_tracks')
      Mopidy.post(json)
    end

    def self.index
      json = Mopidy.format_json(1, 'core.tracklist.index')
      Mopidy.post(json)
    end

    def self.shuffle(start_index, end_index)
      params = { 'start': start_index, 'end': end_index }
      json = Mopidy.format_json(1, 'core.tracklist.shuffle', params)
      Mopidy.post(json)
    end

    def self.tl_tracks
      json = Mopidy.format_json(1, 'core.tracklist.get_tl_tracks')
      Mopidy.post(json)
    end

    def self.add(track)
      json = Mopidy.format_json(1, 'core.tracklist.add', 'uris': [track['uri']])
      Mopidy.post(json)
    end

	  def self.add_uri(uri)
		  json = Mopidy.format_json(1, 'core.tracklist.add', 'uris': [uri])
		  Mopidy.post(json)
	  end

    def self.length
      json = Mopidy.format_json(1, 'core.tracklist.get_length')
      Mopidy.post(json)
    end

    def self.clear
      json = Mopidy.format_json(1, 'core.tracklist.clear')
      Mopidy.post(json)
    end

    def self.repeat
      json = Mopidy.format_json(1, 'core.tracklist.get_repeat')
      Mopidy.post(json)
    end

    def self.repeat=(value)
      json = Mopidy.format_json(1, 'core.tracklist.set_repeat', [!!value])
      Mopidy.post(json)
    end

    def self.single
      json = Mopidy.format_json(1, 'core.tracklist.get_single')
      Mopidy.post(json)
    end

    def self.single=(value)
      json = Mopidy.format_json(1, 'core.tracklist.set_single', [!!value])
      Mopidy.post(json)
    end
  end
end
