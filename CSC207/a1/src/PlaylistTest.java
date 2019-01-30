import static org.junit.Assert.*;


import org.junit.Test;

public class PlaylistTest {

	@Test
	public void testArtistGetName() {
		Artist a = new Artist("Celine Dion", "Canada");
		assertEquals("Celine Dion", a.getName());
	}

	@Test
	public void testArtistGetCountry() {
		Artist a = new Artist("Celine Dion", "Canada");
		assertEquals("Canada", a.getCountry());
	}

	@Test
	public void testGenreGetName() {
		Genre g = new Genre("rock and roll");
		assertEquals("rock and roll", g.getName());
	}

	@Test
	public void testGenreIsPlayedBy() {
		Artist a = new Artist("Celine Dion", "Canada");
		Genre g = new Genre("pop");
		a.addGenre(g);
		assertTrue(g.isPlayedBy(a));
	}

	@Test
	public void testGenreNotPlayedBy() {
		Artist a = new Artist("Celine Dion", "Canada");
		Genre g = new Genre("country");
		assertFalse(g.isPlayedBy(a));
	}

	@Test
	public void testGetGenreOneArtistNoGenre() {
		Artist a = new Artist("Celine Dion", "Canada");
		assertTrue(a.getGenres().size() == 0);
	}

	@Test
	public void testOneArtistAddGenreGetGenres() {
		Artist a = new Artist("Celine Dion", "Canada");
		Genre g = new Genre("pop");
		a.addGenre(g);
		assertTrue(a.getGenres().size() == 1);
		assertTrue(a.getGenres().contains(g));
	}

	@Test
	public void testOneArtistAddArtistGetGenres() {
		Artist a = new Artist("Celine Dion", "Canada");
		Genre g = new Genre("pop");
		g.addArtist(a);
		assertTrue(a.getGenres().size() == 1);
		assertTrue(a.getGenres().contains(g));
		assertTrue(g.isPlayedBy(a));
	}

	@Test
	public void testHasSameArtist() {
		Artist a = new Artist("Celine Dion", "Canada");
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("soft rock");
		a.addGenre(g1);
		a.addGenre(g2);
		assertTrue(g1.hasSameArtist(g2));
	}

	@Test
	public void testNotHasSameArtist() {
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("soft rock");
		assertFalse(g1.hasSameArtist(g2));
	}

	@Test
	public void testOneArtistTwoGenres() {
		Artist a = new Artist("Celine Dion", "Canada");
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("soft rock");
		a.addGenre(g1);
		g2.addArtist(a);

		// Does a contain both Genres?
		assertTrue(a.getGenres().size() == 2);
		assertTrue(a.getGenres().contains(g1));
		assertTrue(a.getGenres().contains(g2));

		// Was each Genre played by the Artist?
		assertTrue(g1.isPlayedBy(a));
		assertTrue(g2.isPlayedBy(a));

		// Were g1 and g2 played by the same Artist?
		assertTrue(g1.hasSameArtist(g2));
		assertTrue(g2.hasSameArtist(g1));
	}

	@Test
	public void testArtistEquals() {
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Celine Dion", "Canada");
		assertTrue(a1.equals(a2));
	}

	@Test
	public void testArtistEqualsDifferentGenres() {
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Celine Dion", "Canada");
		Genre g = new Genre("pop");
		a1.addGenre(g);
		assertTrue(a1.equals(a2));
	}

	@Test
	public void testArtistNotEqualsName() {
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Elvis Presley", "USA");
		assertFalse(a1.equals(a2));
	}

	@Test
	public void testArtistNotEqualsCountry() {
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Celine Dion", "USA");
		assertFalse(a1.equals(a2));
	}

	@Test
	public void testGenreEqualsNoArtists() {
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("pop");
		assertTrue(g1.equals(g2));
	}

	@Test
	public void testGenreNotEqualsTwoGenres() {
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("jazz");
		assertFalse(g1.equals(g2));
	}

	@Test
	public void testGenreNotEqualsNoGenre() {
		Genre g1 = new Genre("rock and roll");
		assertFalse(g1.equals("Not a Genre"));
	}

	@Test
	public void testGenreEqualsTwoArtists() {
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("pop");
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Adele", "UK");
		g1.addArtist(a1);
		g1.addArtist(a2);
		g2.addArtist(a1);
		g2.addArtist(a2);
		assertTrue(g1.equals(g2));
	}

	@Test
	public void testGenreEqualsTwoArtistsDifferentOrder() {
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("pop");
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Adele", "UK");
		g1.addArtist(a1);
		g1.addArtist(a2);
		g2.addArtist(a2);
		g2.addArtist(a1);
		assertTrue(g1.equals(g2));
	}

	@Test
	public void testGenreNotEqualsExtraArtist() {
		Genre g1 = new Genre("pop");
		Genre g2 = new Genre("rock");
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Elvis Presley", "USA");
		Artist a3 = new Artist("Adele", "UK");
		g1.addArtist(a1);
		g1.addArtist(a2);
		g2.addArtist(a2);
		g2.addArtist(a1);
		g2.addArtist(a3);
		assertFalse(g1.equals(g2));
	}

	@Test
	public void testGenreToStringNoArtists() {
		Genre g1 = new Genre("rock");
		String res = g1.toString();
		String exp = "rock ()";
		assertEquals(exp, res);
	}

	@Test
	public void testGenreToStringOneArtist() {
		Genre g1 = new Genre("pop");
		Artist a1 = new Artist("Celine Dion", "Canada");
		g1.addArtist(a1);
		String res = g1.toString();
		String exp = "pop (Celine Dion)";
		assertEquals(exp, res);
	}

	@Test
	public void testGenreToStringThreeArtists() {
		Genre g1 = new Genre("pop");
		Artist a1 = new Artist("Celine Dion", "Canada");
		Artist a2 = new Artist("Elvis Presley", "USA");
		Artist a3 = new Artist("Adele", "UK");
		g1.addArtist(a1);
		g1.addArtist(a2);
		g1.addArtist(a3);
		String res = g1.toString();
		String exp = "pop (Celine Dion, Elvis Presley, Adele)";
		assertEquals(exp, res);
	}

	@Test
	public void testArtistToStringNoGenres() {
		Artist a1 = new Artist("Celine Dion", "Canada");
		String res = a1.toString();
		String exp = "Celine Dion, Canada";
		assertEquals(exp, res);
	}

	@Test
	public void testArtistToStringOneArtist() {
		Genre g1 = new Genre("pop");
		Artist a1 = new Artist("Celine Dion", "Canada");
		g1.addArtist(a1);
		String res = a1.toString();
		String exp = "Celine Dion, Canada" + System.lineSeparator() + g1.getName();
		assertEquals(exp, res);
	}

	@Test
	public void testArtistToStringFourGenres() {
		Genre g1 = new Genre("rock");
		Genre g2 = new Genre("country");
		Genre g3 = new Genre("pop");
		Genre g4 = new Genre("rockabilly");
		Artist a1 = new Artist("Elvis Presley", "USA");
		a1.addGenre(g1);
		a1.addGenre(g2);
		a1.addGenre(g3);
		a1.addGenre(g4);
		String res = a1.toString();
		String exp = "Elvis Presley, USA" + System.lineSeparator() + g1.getName() + System.lineSeparator() + g2.getName()
				+ System.lineSeparator() + g3.getName() + System.lineSeparator() + g4.getName();
		assertEquals(exp, res);
	}

}
