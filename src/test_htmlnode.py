import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('h1', 'Title', '',{"id": "main-title", "class":"test_title"})
        node2 = HTMLNode('h1', 'Title', '',{"id": "main-title", "class":"test_title"}) 
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    

    def test_no_equal(self):
        node3 = HTMLNode('h1', 'Title', '',{"id": "main-title", "class":"test_title"})
        node4 = HTMLNode('h2', 'Sub-title', '',{"id": "main-title", "class":"test_title"})
        self.assertNotEqual(node3, node4) 
    
    def test_eq(self):
        leaf_node = LeafNode(tag="p", value="test_p", props={"id": "p1"})
        self.assertEqual(leaf_node.to_html(), "<p id='p1'>test_p</p>") 
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()