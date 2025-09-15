    public class Food {
      String name;
      Date expirationDate;
      Fridge fridge=null;      
      public Food(String name, Date expirationDate) {
        this.name = name;
        this.expirationDate = expirationDate;
      }
      public Fridge getFridge(){ return fridge; }
    }

    public interface IFridge {
      public void putInFood(Food f);
      public ArrayList<Food> getExpiredFoods();
    }

    public class Fridge implements IFridge {
      private List<Food> foods = new ArrayList<>();      
      public void putInFood(Food f) {
        // if (f != null && !foods.contains(f))
        f.fridge=this;
        foods.add(f);
      }
      public ArrayList<Food> getExpiredFoods() {
        ArrayList<Food> expiredFoods = new ArrayList<>();
        Date now = Date.from(Instant.now());
        for (Food food : foods)
	        if (food.expirationDate.before(now))
		        expiredFoods.add(food);
        foods.removeAll(expiredFoods);
        return expiredFoods;
      }
      public Food searchFoodByName(String name) {
        // for each food in foods, return food if name is equal
        for (Food food : foods) if (food.name.equals(name)) return food;
        return null;
      }
      public boolean takeOut(Food food) {
        return foods.remove(food);
      }
    }
