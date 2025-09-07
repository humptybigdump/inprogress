package task1;

public class Item {
    private static final String INFORMATION = "One %s for %d,- €";

    private final String name;
    private final int price;

    public Item(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (other == null || getClass() != other.getClass()) return false;
        Item item = (Item) other;
        return price == item.price && name.equals(item.name);
    }

    @Override
    public String toString() {
        return String.format(INFORMATION, name, price);
    }
}
