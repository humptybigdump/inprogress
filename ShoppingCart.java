package task1;

public interface ShoppingCart {
    boolean addItem(Item item);
    boolean removeItem(Item item);
    double getTotalSum();
    void printShoppingCart();
}
