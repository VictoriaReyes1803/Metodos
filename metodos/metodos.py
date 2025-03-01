
import numpy as np
import sympy as sp

def euler_mejorado(f_expr, x0, y0, h, n, xf,decimales=None):
    x, y = sp.symbols('x y')
    f = sp.sympify(f_expr)  
    print (f)
    f_lambda = sp.lambdify((x, y), f, 'math')
    print(xf)
    resultados = []
    
    for i in range(n):
        f_xn_yn = float(f_lambda(x0, y0)) 
        y_pred = float(y0 + h * f_xn_yn)  
        f_xnp1_ypred = float(f_lambda(x0 + h, y_pred))  
        y_corr = float(y0 + (h / 2) * (f_xn_yn + f_xnp1_ypred))  
        
        x_next = float(x0 + h)  

        if decimales is not None:
            x_next = round(x_next, decimales)
            y_corr = round(y_corr, decimales)
            f_xn_yn = round(f_xn_yn, decimales)
            y_pred = round(y_pred, decimales)
            f_xnp1_ypred = round(f_xnp1_ypred, decimales)

        resultados.append({
            'iteracion': i,
            'x': x0,
            'y': y0,
            'f_xn_yn': f_xn_yn,
            'y_pred': y_pred,
            'f_xnp1_ypred': f_xnp1_ypred,
            'y_corr': y_corr
        })
        
        x0 = x_next
        y0 = y_corr
    print (resultados)
    return resultados


def runge_kutta(f_expr, x0, y0, h, n,actual_solution=None,decimales=None):
    x, y = sp.symbols('x y')
    f = sp.sympify(f_expr)  
    print (f)
    f_lambda = sp.lambdify((x, y), f, 'math')

    resultados = []
    for i in range(n):
        k1 = h * f_lambda(x0, y0)
        k2 = h * f_lambda(x0 + h / 2, y0 + k1 / 2)
        k3 = h * f_lambda(x0 + h / 2, y0 + k2 / 2)
        k4 = h * f_lambda(x0 + h, y0 + k3)
        yn = y0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x_next = x0 + h
        
        error_absoluto = abs(actual_solution(x_next) - yn) if actual_solution else None
        
        if decimales is not None:
            x_next = round(x_next, decimales)
            yn = round(yn, decimales)
            k1 = round(k1, decimales)
            k2 = round(k2, decimales)
            k3 = round(k3, decimales)
            k4 = round(k4, decimales)
            if error_absoluto is not None:
                error_absoluto = round(error_absoluto, decimales)
                
        resultados.append({
            'i': i,
            'x': x_next,
            'y': yn,
            'error_absoluto': error_absoluto,
            'k1': k1,
            'k2': k2,
            'k3': k3,
            'k4': k4
        })
        
        x0 = x_next
        y0 = yn
    print ('resultados',resultados)
    return resultados


def newton_raphson(f_expr, x0, tol=1e-5, max_iter=100):
    x = sp.symbols('x')
    f = sp.sympify(f_expr)  
    df = sp.diff(f, x)  

    f_lambda = sp.lambdify(x, f, 'math')  
    df_lambda = sp.lambdify(x, df, 'math')

    iteraciones = []

    for i in range(1, max_iter + 1):
        fx = f_lambda(x0)
        dfx = df_lambda(x0)

        if dfx == 0:
            return "Error: La derivada es cero en x = {:.6f}".format(x0), iteraciones

        x1 = x0 - fx / dfx

        iteraciones.append({
            "iter": i,
            "x": round(x0, 6),
            "fx": round(fx, 6),
            "dfx": round(dfx, 6)
        })

        if abs(x1 - x0) < tol:
            return round(x1, 6), iteraciones
        
        x0 = x1
    
    return "No convergió en {} iteraciones".format(max_iter), iteraciones