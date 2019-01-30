package strategy;

import java.io.FileNotFoundException;

public class Main {
    
    public static void main(String[] args) throws FileNotFoundException {
        
        Sorter<Book> sorter1 = new InsertionSorter<Book>();
        Sorter<Book> sorter2 = new SelectionSorter<Book>();

        Author author1 = new Author("J.K. Rowling", sorter1);
        Author author2 = new Author("Stephen King", sorter2);
                
        Book b1 = new Book("Harry Potter", "1770893083");
        Book b2 = new Book("The Shining", "1443433659");
        Book b3 = new Book("Fantastic Beasts", "1770891048");
        Book b4 = new Book("Quidditch Through The Ages", "0385659768");
        Book b5 = new Book("Carrie", "0006485456");
        
        author1.addBook(b1);
        author1.addBook(b3);
        author1.addBook(b4);
        
        author2.addBook(b2);
        author2.addBook(b5);
        
        author1.sortBooks();
        System.out.println(author1.toString());
        
        author2.sortBooks();
        System.out.println(author2.toString());

    }
}