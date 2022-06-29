package Java.Iterator;

public class IteratorExample {
    public static void main(String[] args) {
        Company company = new Company();
        for (Iterator iter = company.getIterator(); iter.hasNext();) {
            System.out.println("Name " + iter.next());
        }
    }
}
