import java.util.ArrayList;
import java.util.List;

public class TreeNode<T> {
    private T value;
    private TreeNode<T> parent;
    private List<TreeNode<T>> children;

    public TreeNode(T value, TreeNode<T> parent) {
        this.value = value;
        this.parent = parent;
        this.children = new ArrayList<>();
    }

    public boolean addChild(TreeNode<T> child) {
        return this.children.add(child);
    }

    public TreeNode<T> getChild(int index) {
        return this.children.get(index);
    }

    public void setParent(TreeNode<T> parent) {
        this.parent = parent;
    }

    public boolean areChildrenEmpty() {
        return this.children.isEmpty();
    }
}

