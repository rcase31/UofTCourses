import java.util.ArrayList;

public class Artist {
	private String name;
	private ArrayList<Genre> genres;
	private String country;

	/**
	 * 	When a star is born...
	 * @param name		The name of this artist.
	 * @param country	The country where this artist was born or performs in.
	 */
	public Artist(String name, String country) {
		this.name = name;
		this.country = country;
		this.genres = new ArrayList();

	}

    /**
     *	This method will check whether a given Genre is already in an artist's list.
     * @param g2BeChecked	Genre that will be looked for in this artist's list.
     * @return	Whether or not the genre is in the artist's list.
     */
    private boolean checkGenreList(Genre g2BeChecked){
        for (Genre g: genres){
            if (g.getName().equals(g2BeChecked.getName()))
                return true;
        }
        return false;
    }

	/**
	 * 	We add a genre to this artist. This genre will be stored in the artist's list.
	 * @param newGenre	The new genre to be added to this artist's  list.
	 */
	public void addGenre(Genre newGenre){
		if (!checkGenreList(newGenre)) {
			this.genres.add(newGenre);
			newGenre.addArtist(this);
		}
	}

	public ArrayList getGenres(){
		return this.genres;
	}

	public String getName(){
		return this.name;
	}

	public String getCountry() {
		return country;
	}

	/**
	 * 	Compares two artists. Checks whether they are the same person. For them to be equal, their names must match,
	 * 	and so do their countries.
	 * @param artist	An artist to be compared.
	 * @return	Whether both artists are the same.
	 */
	public boolean equals(Artist artist){
		return (this.name.equals(artist.name) && this.country.equals(artist.country));
	}

	@Override
	public String toString(){

		String[] strGenres = new String[genres.size()];
		int i = 0;
		for (Genre g: genres){
			strGenres[i++] = g.getName();
		}

		String ret = this.name + ", " + this.country;
		if (strGenres.length != 0)
			ret += System.lineSeparator() + String.join(System.lineSeparator(), strGenres);
		return ret;

	}

}
