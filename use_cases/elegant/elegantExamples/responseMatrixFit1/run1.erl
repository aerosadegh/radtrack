SDDS1
&description text="Error log--input: run1.ele  lattice: par.lte", contents="error log, elegant output" &end
&associate filename="run1.ele", path="/home/oxygen/BORLAND/elegantExamples/responseMatrixFit1", contents="elegant input, parent" &end
&associate filename="par.lte", path="/home/oxygen/BORLAND/elegantExamples/responseMatrixFit1", contents="elegant lattice, parent" &end
&parameter name=Step, type=long, description="simulation step" &end
&parameter name=When, type=string, description="phase of simulation when errors were asserted" &end
&column name=ParameterValue, type=double, description="Perturbed value" &end
&column name=ParameterError, type=double, description="Perturbation value" &end
&column name=ElementParameter, type=string, description="Parameter name" &end
&column name=ElementName, type=string, description="Element name" &end
&column name=ElementOccurence, type=long, description="Element occurence" &end
&column name=ElementType, type=string, description="Element type" &end
&data mode=ascii, lines_per_row=1, no_row_counts=1 &end
0              ! simulation step
pre-correction
-1.282581654870910e-03 -1.282581654870910e-03        FSE       P2Q1 1       QUAD
7.068659469357893e-03 7.068659469357893e-03        FSE       P2Q2 1       QUAD
-5.640209350156598e-03 -5.640209350156598e-03        FSE       P2Q3 1       QUAD
-1.288662128684621e-02 -1.288662128684621e-02        FSE       P2Q4 1       QUAD
1.605455626021007e-02 1.605455626021007e-02        FSE       P3Q4 1       QUAD
-4.163158417173311e-03 -4.163158417173311e-03        FSE       P3Q3 1       QUAD
8.994721936387494e-03 8.994721936387494e-03        FSE       P3Q2 1       QUAD
-4.373001225479761e-03 -4.373001225479761e-03        FSE       P3Q1 1       QUAD
-7.382923773053776e-03 -7.382923773053776e-03        FSE       P4Q1 1       QUAD
6.064359402805356e-03 6.064359402805356e-03        FSE       P4Q2 1       QUAD
1.507542128317545e-02 1.507542128317545e-02        FSE       P4Q3 1       QUAD
4.194885289699786e-03 4.194885289699786e-03        FSE       P4Q4 1       QUAD
-3.813669235246583e-03 -3.813669235246583e-03        FSE       P1Q4 1       QUAD
-2.560850612084234e-03 -2.560850612084234e-03        FSE       P1Q3 1       QUAD
-1.617768335059414e-02 -1.617768335059414e-02        FSE       P1Q2 1       QUAD
-1.266901829210041e-03 -1.266901829210041e-03        FSE       P1Q1 1       QUAD

