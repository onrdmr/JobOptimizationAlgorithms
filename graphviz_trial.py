import graphviz

# Define the graph
dot = graphviz.Digraph()

# Add a node with multiple cells
# Add a node with multiple cells
table = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD>Cell 1</TD>
    <TD>Cell 2</TD>
  </TR>
  <TR>
    <TD COLSPAN="2">
      <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD>Deneme</TD></TR>
      </TABLE>
    </TD>
  </TR>
  <TR>
    <TD>Cell 1</TD>
    <TD>Cell 2</TD>
  </TR>
</TABLE>>'''
dot.node('A', label=table)

# Render the graph
dot.render('example', format='png')