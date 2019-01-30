
import java.util.ArrayList;

public class Genre {
	private String name;
	private ArrayList<Artist> artists;

	/**
	 * Auxiliary method that returns one artist from the list stored in this genre.
	 * @param j	This is the index to where the artist is placed on the list.
	 * @return	The artist at index j.
	 */
	public Artist getArtist(int j){
		return artists.get(j);
	}

	/**
	 * Auxiliary method to check whether a given artist is already on this genre's list.
	 * We do this to avoid duplicate entries.
	 * @param a2BeChecked	The artist we need to verify.
	 * @return	Whether or not the artist was already on this genre's list.
	 */
	private boolean checkArtistList(Artist a2BeChecked){
		for (Artist a: artists){
			if (a.equals(a2BeChecked))
					return true;
		}
		return false;
	}

	/**
	 * Our constructor.
	 * @param name This genre name.
	 */
	public Genre(String name) {
		this.name = name;
		this.artists = new ArrayList();
	}

	/**
	 * Checks whether this genre is played by a given artist.
	 * @param artist	The artist we need checking.
	 * @return	Does this artist play this genre?
	 */
	public boolean isPlayedBy(Artist artist){
		for (Artist a: artists){
			if (a.equals(artist))
				return true;
		}
		return false;
	}

	public String getName() {
		return this.name;
	}

	/**
	 * We add a new artist to the list of artists in this genre, avoiding duplicates.
	 * @param newArtist	The artist that may be added to artists.
	 */
	public void addArtist(Artist newArtist){
		if (!checkArtistList(newArtist)) {
			this.artists.add(newArtist);
			newArtist.addGenre(this);
		}
	}

	/**
	 * Checks whether 2 genres share at least one artist in common.
	 * @param genre	The other genre to be compared to this one.
	 * @return	Do they share at least one artist? The answer lies on this method...
	 */
	public boolean hasSameArtist(Genre genre){
		for (Artist art: artists){
			if (genre.artists.contains(art))
				return true;
		}
		return false;
	}

	/**
	 * We compare two genres and check whether they are equal. In order for them to be equal, all artists must be
	 * same, and both genres name must also be the same.
	 * @param genre	The other genre we need to check equality.
	 * @return	Are they equal? true for yes, false for no.
	 */
	public boolean equals(Genre genre){
		if (this.name.equals(genre.name)){
			for (Object artist: artists){
				if (!genre.artists.contains(artist))
					return false;
			}
			return true;
		}
		return false;
	}

	@Override
	public String toString(){
		String[] vTemp = new String[artists.size()];
		int i = 0;
		for (Artist artist: artists){
			vTemp[i++] = artist.getName();
		}
		String ret = name + " (";
		if (vTemp.length != 0)
			ret += String.join(", ", vTemp);
		ret += ")";
		return ret;

	}
}
