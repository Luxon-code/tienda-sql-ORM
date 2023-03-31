from app import app
from models.producto import *
from models.categoria import *
from flask import render_template,request,redirect
from sqlalchemy import exc
from werkzeug.utils import secure_filename
import os
@app.route('/')
def listarProductos():
    mensaje = "lista de productos"
    try:
        listaProductos = Producto.query.all()
    except exc.SQLAlchemyError as error:
        mensaje = str(error)
    return render_template('listarProductos.html',listaProductos=listaProductos,mensaje=mensaje)

@app.route('/api/listarProductos')
def api_listarProductos():
    try:
        listaProductos = Producto.query.all()
        listaJson =  []
        for producto in listaProductos:
            p = {
                "idProducto": producto.idProducto
            }
            listaJson.append(p)
    except exc.SQLAlchemyError as error:
        mensaje = str(error)
    return listaJson
@app.route('/vistaAgregarProducto')
def vistaAgregarProductos():
    producto = None
    listaCategorias = Categoria.query.all()
    return render_template("frmAgregarProducto.html",producto=producto,listaCategorias=listaCategorias)
@app.route('/agregarProducto', methods= ["POST"])
def agregarProducto():
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombre"]
        precio = int(request.form["txtPrecio"])
        categoria = request.form["cbCategoria"]
        
        producto = Producto(proCodigo=codigo,proNombre=nombre,proPrecio=precio,proCategoria=categoria)
        db.session.add(producto)
        db.session.commit()
        archivo = request.files["fileFoto"]
        nombreArchivo = secure_filename(archivo.filename)
        listaNombreArchivo = nombreArchivo.rsplit(".",1)
        extension = listaNombreArchivo[1].lower()
        nuevoNombre = str(producto.idProducto)+"."+extension
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'],nuevoNombre))
        mensaje = "Producto agregado Correctamente"
        return redirect('/') and render_template("listarProductos.html",mensaje=mensaje,listaProductos = Producto.query.all())
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = "ya existe un producto con este codigo"
    return render_template("frmAgregarProducto.html",mensaje=mensaje,producto=producto,listaCategorias = Categoria.query.all())
@app.route('/consultar/<int:idProducto>',methods=["GET"])
def consultarProductoPorId(idProducto):
    try:
        producto  =Producto.query.get(idProducto)
    except exc.SQLAlchemyError as error:
        mensaje = str(error)
    return render_template("frmEditarProducto.html",producto=producto,listaCategorias = Categoria.query.all())
@app.route('/actualizarProducto',methods=["POST"])
def actualizarProducto():
    try:
        idProducto = request.form['idProducto']
        producto = Producto.query.get(idProducto)
        producto.proCodigo = request.form["txtCodigo"]
        producto.proNombre = request.form["txtNombre"]
        producto.proPrecio = request.form["txtPrecio"]
        producto.proCategoria = request.form["cbCategoria"]
        db.session.commit()
        archivo = request.files["fileFoto"]
        if archivo.filename!="":
            nombreArchivo = secure_filename(archivo.filename)
            listaNombreArchivo = nombreArchivo.rsplit(".",1)
            extension = listaNombreArchivo[1].lower()
            nuevoNombre = str(producto.idProducto)+"."+extension
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'],nuevoNombre))
        mensaje = "Producto Actualizado"
        return redirect("/")
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = str(error)
    return render_template("frmEditarProducto.html",producto = producto,listaCategorias = Categoria.query.all())
@app.route('/eliminar/<int:idProducto>',methods=["GET"]) 
def eliminarProducto(idProducto):
    try:
        db.session.query(Producto).filter(Producto.idProducto == idProducto).delete()
        db.session.commit()
        os.remove(app.config["UPLOAD_FOLDER"]+"/"+str(idProducto)+".jpg")
        mensaje = "Producto Eliminado Correctamente"
    except exc.SQLAlchemyError as error:
        mensaje = str(error)
    return render_template("listarProductos.html",listaProductos = Producto.query.all(),mensaje=mensaje)      