package Java.Iterator;

public class Company implements Iterator {
    private String names[] = { "Google", "Facebook", "Amazon" };
    private int index;

    @Override
    public Iterator getIterator() {
        return new Company();
    }

    @Override
    public boolean hasNext() {
        if (index < names.length)
            return true;
        return false;
    }

    @Override
    public String next() {
        if (this.hasNext())
            return names[index++];
        return null;
    }

}
