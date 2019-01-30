/**
 *
 */

import java.util.ArrayList;
import java.util.Scanner;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * The Playlist Class.
 */
public class Playlist {

    /**
     * All possible responses to the user's input on the command line.
     */
    private enum Actions{
        VALID, INVALID, EXIT
    }

    private static String linePrint;
    private static GenreList genreList = new GenreList();


	public static void main(String[] args) {
        // We put all genres in our list, so we only have to read the file once.
        LoadAllArtistsAndGenres(genreList);
        Scanner inputText = new Scanner(System.in);
	    while(true){
            System.out.println("Enter a genre.");
            String inputLine = inputText.nextLine();
            switch (responseToInput(inputLine)){
                case EXIT:
                    return;
                case VALID:
                case INVALID:
                    System.out.println(linePrint);
                    break;
            }

        }
	}

    /**
     * This method will check whether the input is a valid genre. If it is a valid one, it will save the line to be
     * printed for later use in the main method.
     * @param input User keyboard input.
     * @return  Returns whether a valid genre was input.
     */
	private static boolean isValidGenre(String input){
        Genre searchedOne = genreList.getGenreByName(input);
        if (searchedOne == null){
            linePrint = "This is not a valid genre.";
        }else {
            linePrint = searchedOne.toString();
        }

        return false;

    }

    /**
     * Interprets the user keyboard input.
     * @param input User keyboard input.
     * @return  Returns what kind of input has the user entered.
     */
    private static Actions responseToInput(String input){
	    if (input.equals("exit"))
	        return Actions.EXIT;
	    if (isValidGenre(input)){
	        return Actions.VALID;
        }else {
	        return Actions.INVALID;
        }

    }

    /**
     * This method will read (only once) the text file "Music.txt" and load the genreList from this class.
     * @param genreList This is the list of all genres listed on "Music.txt". It will be loaded on this method.
     */
    private static void LoadAllArtistsAndGenres(GenreList genreList){
	    ArrayList<String> vTemp = FileHandle.readMusicTxt();
	    Artist artTemp;
	    Genre genTemp;
	    String[] vLineComma;
	    String[] vLineBarr;
	    String country;


	    for (String line: vTemp){
	        vLineComma = line.split(",");
	        vLineBarr = line.split("\\|");


	        if ((vLineComma.length > 1) && (vLineBarr.length > 1)){
	            country = vLineComma[1].split(" ")[1];
                artTemp = new Artist(vLineComma[0], country);

                // Now we must add the genres for this artist
                for (int i = 1; i < vLineBarr.length; i++){
                    genTemp = new Genre(vLineBarr[i].trim());
                    artTemp.addGenre(genTemp);
                    genreList.addGenre(genTemp);
                }

            }

        }

    }
}


/**
 * This class is designed specifically to store the genres listed on Music.txt, and all their related artists.
 */
class GenreList{

    private ArrayList<Genre> genres;

    public GenreList(){
        genres = new ArrayList();
    }

    /**
     * Checks whether a genre is already in the genreList. When the genre is the same as some already on the list,
     * we will add the new artist to that genre.
     * @param g2BeChecked Genre to be checked.
     * @return  whether or not the genre already was on the list.
     */
    private boolean checkGenreList(Genre g2BeChecked){
        for (Genre g: genres){
            if (g.getName().equals(g2BeChecked.getName())) {
                // Since the genres are the same, we add the new artist to the genre's list.
                addArtistToThisGenre(g, g2BeChecked);
                return true;
            }
        }
        return false;
    }

    public Genre getGenreByName(String genreName){

        for (Genre g: genres){
            if (g.getName().equals(genreName)){
                return g;
            }
        }
        return null;
    }

    public void addGenre(Genre newGenre){
        /**
         * We must check whether there already is such a Genre on our list.
         * If there isn't, we add to it.
         */
        if (!checkGenreList(newGenre))
            this.genres.add(newGenre);
    }

    /**
     * This method adds the artist from g2 to the g1's list.
     * Precondition: g2 has only one artist.
     * @param g1    First input genre.
     * @param g2    Second input genre.
     */
    private void addArtistToThisGenre(Genre g1, Genre g2){
        g1.addArtist(g2.getArtist(0));
    }

}

//class ArtistList{
//
//    private ArrayList<Artist> artists;
//
//    public ArtistList(){
//        artists = new ArrayList<Artist>();
//    }
//
//    public void addArtist(Artist newArtie){
//        for (Artist tempArtie: artists){
//            if (tempArtie.equals(newArtie)){
//                tempArtie.mergeGenres(newArtie);
//                newArtie = tempArtie;
//                // VAI DAR MERDA PORQUE DAI PERDE O ENDERECO ANTIGO... PONTEIRO DE PONTEIRO??
//            }
//        }
//
//    }
//}


/**
 * A class designed to handle files.
 */
class FileHandle {
    private static final String fileName = "Music.txt";

    /**
     * This method is designed specifically to open and read "Music.txt".
     * @return  Returns an ArrayList of all lines of "Music.txt"
     */
    public static ArrayList<String> readMusicTxt() {

        ArrayList<String> output = new ArrayList<>();

        try (BufferedReader fileReader = new BufferedReader(new FileReader(fileName))) {

            String line = fileReader.readLine();

            while (line != null) {
                output.add(line);
                line = fileReader.readLine();
            }
            return output;
        }catch(IOException iox){
            System.out.println("We apologise the inconvenience, but no Music.txt as found.");
        }
        return output;
    }
}