import streamlit as st
from streamlit import StreamlitAPIException

from tests import testutil


class ColumnsTest(testutil.DeltaGeneratorTestCase):
    """Test columns."""

    def test_equal_width_columns(self):
        """Test that it works correctly when spec is int"""
        columns = st.columns(3)

        for column in columns:
            with column:
                st.write("Hello")

        all_deltas = self.get_all_deltas_from_queue()

        horizontal_block = all_deltas[0]
        columns_blocks = all_deltas[1:4]
        widgets = all_deltas[4:]
        # 7 elements will be created: 1 horizontal block, 3 columns, 3 markdown
        self.assertEqual(len(all_deltas), 7)
        self.assertEqual(columns_blocks[0].add_block.column.weight, 1.0 / 3)
        self.assertEqual(columns_blocks[1].add_block.column.weight, 1.0 / 3)
        self.assertEqual(columns_blocks[2].add_block.column.weight, 1.0 / 3)

    def test_not_equal_width_int_columns(self):
        """Test that it works correctly when spec is list of ints"""
        weights = [3, 2, 1]
        sum_weights = sum(weights)
        columns = st.columns(weights)

        for column in columns:
            with column:
                st.write("Hello")

        all_deltas = self.get_all_deltas_from_queue()

        horizontal_block = all_deltas[0]
        columns_blocks = all_deltas[1:4]
        widgets = all_deltas[4:]
        # 7 elements will be created: 1 horizontal block, 3 columns, 3 markdown
        self.assertEqual(len(all_deltas), 7)
        self.assertEqual(columns_blocks[0].add_block.column.weight, 3.0 / sum_weights)
        self.assertEqual(columns_blocks[1].add_block.column.weight, 2.0 / sum_weights)
        self.assertEqual(columns_blocks[2].add_block.column.weight, 1.0 / sum_weights)

    def test_not_equal_width_float_columns(self):
        """Test that it works correctly when spec is list of floats or ints"""
        weights = [7.5, 2.5, 5]
        sum_weights = sum(weights)
        columns = st.columns(weights)

        for column in columns:
            with column:
                pass

        all_deltas = self.get_all_deltas_from_queue()

        horizontal_block = all_deltas[0]
        columns_blocks = all_deltas[1:]
        # 4 elements will be created: 1 horizontal block, 3 columns
        self.assertEqual(len(all_deltas), 4)
        self.assertEqual(len(columns_blocks), 3)
        self.assertEqual(columns_blocks[0].add_block.column.weight, 7.5 / sum_weights)
        self.assertEqual(columns_blocks[1].add_block.column.weight, 2.5 / sum_weights)
        self.assertEqual(columns_blocks[2].add_block.column.weight, 5.0 / sum_weights)


class ExpanderTest(testutil.DeltaGeneratorTestCase):
    def test_label_required(self):
        """Test that label is required"""
        with self.assertRaises(TypeError):
            expander = st.expander()

    def test_just_label(self):
        """Test that it can be called with no params"""
        expander = st.expander("label")

        with expander:
            pass

        expander_block = self.get_delta_from_queue()
        self.assertEqual(expander_block.add_block.expandable.label, "label")
        self.assertEqual(expander_block.add_block.expandable.expanded, False)


class TabsTest(testutil.DeltaGeneratorTestCase):
    def test_tab_required(self):
        """Test that atleast one tab is required."""
        with self.assertRaises(TypeError):
            tabs = st.tabs()

        with self.assertRaises(StreamlitAPIException):
            tabs = st.tabs([])

    def test_only_label_strings_allowed(self):
        """Test that only strings are allowed as tab labels."""
        with self.assertRaises(StreamlitAPIException):
            tabs = st.tabs(["tab1", True])

        with self.assertRaises(StreamlitAPIException):
            tabs = st.tabs(["tab1", 10])

    def test_returns_all_expected_tabs(self):
        """Test that all labels are added in correct order."""
        tabs = st.tabs([f"tab {i}" for i in range(5)])

        self.assertEqual(len(tabs), 5)

        for tab in tabs:
            with tab:
                pass

        all_deltas = self.get_all_deltas_from_queue()

        horizontal_block = all_deltas[0]
        tabs_block = all_deltas[1:]
        # 6 elements will be created: 1 horizontal block, 5 tabs
        self.assertEqual(len(all_deltas), 6)
        self.assertEqual(len(tabs_block), 5)
        for index, tabs_block in enumerate(tabs_block):
            self.assertEqual(tabs_block.add_block.tab.label, f"tab {index}")
