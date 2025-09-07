package task1;

public class Main {
    public static void main(String[] args) {
        ShoppingCart myShoppingCart = new MyShoppingCart();

        myShoppingCart.addItem(new Item("Banana", 1));
        myShoppingCart.addItem(new Item("Milk", 2));
        myShoppingCart.addItem(new Item("Chocolate", 5));
        myShoppingCart.addItem(new Item("Apple", 3));

        myShoppingCart.removeItem(new Item("Banana", 1));
        myShoppingCart.removeItem(new Item("Milk", 2));
        myShoppingCart.removeItem(new Item("Kebab", 7));

        myShoppingCart.printShoppingCart();
    }
}
