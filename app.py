from flask import Flask, render_template, request
from metodos.metodos import euler_mejorado, runge_kutta, newton_raphson
import re
import sympy as sp
import math
from parse import procesar_funcion
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/euler', methods=['GET', 'POST'])
def euler():
    resultado = None
    if request.method == 'POST':
        try:
            funcion = request.form["funcion"]
            funcion = procesar_funcion(funcion)   
            x0 = float(request.form["x0"])
            y0 = float(request.form["y0"])
            h = float(request.form["h"])
            
            xf = float(request.form["xf"])
            decimales = int(float(request.form['decimales'])) if request.form.get('decimales') else 6
            n = int((xf - x0) / h)
            print(n)
            resultado = euler_mejorado(funcion, x0, y0, h, n, xf,decimales=decimales)

        except Exception as e:
            resultado = f"Error: {str(e)}"

    return render_template('euler.html', resultado=resultado)

def actual_solution(fx, x0=0, y0=0):
    x = sp.Symbol('x')
    y_general = sp.integrate(fx, x) + sp.Symbol('C')
    C_value = sp.solve(y_general.subs(x, x0) - y0, sp.Symbol('C'))[0]
    y_exact = y_general.subs(sp.Symbol('C'), C_value)
    
    y_func = sp.lambdify(x, y_exact, 'numpy')
    
    return y_func


@app.route('/runge-kutta', methods=['GET', 'POST'])
def runge_kutta_view():
    resultado = None
    if request.method == 'POST':
        funcion = request.form.get("funcion")
        

        if funcion:
            try:
                funcion = procesar_funcion(funcion)
                x0 = float(request.form['x0'])
                y0 = float(request.form['y0'])
                h = float(request.form['h'])
                xf = float(request.form['xf'])
                n = int((xf - x0) / h) 
                decimales = int(float(request.form['decimales'])) if request.form.get('decimales') else 6
                
                resultado = runge_kutta(funcion, x0, y0, h, n, actual_solution(funcion, x0, y0),decimales=decimales)
            except Exception as e:
                resultado = f"Error al evaluar la función: {str(e)}"

    return render_template('runge_kutta.html', resultado=resultado)

@app.route('/newton-raphson', methods=['GET', 'POST'])
def newton_raphson_view():
    resultado = None
    iteraciones = None

    if request.method == 'POST':
        funcion = request.form.get("funcion")
        x0 = float(request.form['x0'])
        tol = float(request.form.get("tol", 1e-5)) 

        if funcion and x0 is not None:
            funcion = procesar_funcion(funcion) 

            try:
                resultado, iteraciones = newton_raphson(funcion, x0, tol)
            except Exception as e:
                resultado = f"Error al evaluar la función: {str(e)}"

    return render_template('newton_raphson.html', resultado=resultado, iteraciones=iteraciones)


if __name__ == '__main__':
    app.run(debug=True)
