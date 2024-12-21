import unittest
from visual import read_config, read_dependencies, get_transitive_dependencies, visualize_graph


class TestDependencyVisualizer(unittest.TestCase):

    def setUp(self):
        self.dependencies_content = """\
matplotlib:
  - contourpy
  - cycler
  - fonttools
  - kiwisolver
  - numpy
  - packaging
  - pillow
  - pyparsing
  - python-dateutil
  - meson-python
  - pybind11
  - setuptools_scm
  - setuptools
"""
        self.dependencies_file = 'test_dependencies.yml'
        with open(self.dependencies_file, 'w') as f:
            f.write(self.dependencies_content)

    def test_read_dependencies(self):
        dependencies = read_dependencies(self.dependencies_file)
        self.assertIn('matplotlib', dependencies)
        self.assertIn('numpy', dependencies['matplotlib'])
        self.assertIn('cycler', dependencies['matplotlib'])

    def test_get_transitive_dependencies(self):
        dependencies = read_dependencies(self.dependencies_file)
        transitive_deps = get_transitive_dependencies('matplotlib', dependencies)

        expected_deps = {
            'contourpy', 'cycler', 'numpy', 'fonttools',
            'kiwisolver', 'packaging', 'pillow',
            'pyparsing', 'python-dateutil', 'meson-python',
            'pybind11', 'setuptools', 'setuptools_scm'
        }

        self.assertEqual(transitive_deps, expected_deps)

    def test_visualize_graph(self):
        dependencies = read_dependencies(self.dependencies_file)
        output = visualize_graph('matplotlib', dependencies)

        self.assertIn("graph TD", output)
        for dep in ['contourpy', 'cycler', 'numpy', 'fonttools', 'kiwisolver', 'packaging', 'pillow', 'pyparsing',
                    'python-dateutil', 'meson-python', 'pybind11', 'setuptools', 'setuptools_scm']:
            self.assertIn(f"matplotlib --> {dep}", output)

    def test_visualize_graph_without_versions(self):
        dependencies = {
            "matplotlib": ["numpy", "pillow", "cycler"],
            "numpy": ["wheel"],
        }
        output = visualize_graph("matplotlib", dependencies)
        self.assertIn("graph TD", output)
        self.assertIn("matplotlib --> numpy", output)
        self.assertNotIn("matplotlib --> numpy==", output)

    def tearDown(self):
        import os
        os.remove(self.dependencies_file)


if __name__ == '__main__':
    unittest.main()
