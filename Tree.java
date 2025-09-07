public class Tree<T> {
    private TreeNode<T> root;

    public Tree() {
        this.root = null;
    }
    public void setRoot(T value) {
        this.root = new TreeNode<>(value, null);
    }

    public TreeNode<T> add(T value, TreeNode<T> parent) {
        TreeNode<T> newNode = new TreeNode<>(value, parent);
        parent.addChild(newNode);
        return newNode;
    }

    public void initializeBubbling(TreeNode<T> newRoot) {
        if (newRoot == null) return;

        TreeNode<T> oldRoot = this.root;
        this.root = newRoot;

        if (oldRoot != null) {
            bubbleDown(oldRoot, newRoot);
        }
    }

    private void bubbleDown(TreeNode<T> node, TreeNode<T> parent) {
        //TODO: implement recursive bubble Down Method
    }
}
