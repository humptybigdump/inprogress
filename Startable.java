package task5;

interface Startable {
    void start();
    void startDelayed(int minutes);
}

abstract class AbstractActuator implements Startable {
    public abstract int getRevolutions();
    public void calibrate() {
        // ...
    }

    @Override
    public void startDelayed(int minutes) {
        // ...
    }
}

class MyMotor extends AbstractActuator {
    @Override
    public int getRevolutions() {
        // ...
    }

    @Override
    public void start() {
        // ...
    }
}
