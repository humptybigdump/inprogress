package task1;

import java.util.ArrayList;
import java.util.List;

public class MyShoppingCart implements ShoppingCart {
    private final List<Item> items = new ArrayList<>();

    @Override
    public boolean addItem(Item item) {
        return items.add(item);
    }

    @Override
    public boolean removeItem(Item item) {
        return items.remove(item);
    }

    @Override
    public double getTotalSum() {
        double sum = 0;
        for (Item item : items) {
            sum += item.getPrice();
        }
        return sum;
    }

    @Override
    public void printShoppingCart() {
        for (Item item : items) {
            System.out.println(item);
        }
    }
}
