import matlab.engine

eng = matlab.engine.start_matlab()

inp = "1/(1-3*x)^2"

eng.FGO(inp,nargout=0)