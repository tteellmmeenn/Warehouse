from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Item
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret-key'  # Flash message ажиллуулахад шаардлагатай
db.init_app(app)

# Өгөгдлийн сан үүсгэх
with app.app_context():
    db.create_all()

# Нүүр хуудас - хайлт хийх боломжтой
@app.route('/', methods=['GET', 'POST'])
def web_view():
    search_query = request.form.get('search', '').strip()
    if search_query:
        items = Item.query.filter(
            (Item.sku.like(f'%{search_query}%')) |
            (Item.name.like(f'%{search_query}%'))
        ).all()
    else:
        items = Item.query.all()
    return render_template('items.html', items=items, search_query=search_query)

# Шинэ бараа нэмэх
@app.route('/items/new', methods=['GET', 'POST'])
def add_item_web():
    if request.method == 'POST':
        try:
            data = request.form
            # quantity ба price шалгах
            quantity = int(data['quantity'])
            price = float(data['price'])
            if quantity < 0 or price < 0:
                flash('Тоо хэмжээ болон үнэ нь 0-с бага байж болохгүй!')
                return redirect(url_for('add_item_web'))

            new_item = Item(
                sku=data['sku'],
                name=data['name'],
                quantity=quantity,
                location=data['location'],
                brand=data['brand'],
                model_no=data['model_no'],
                price=price,
                warranty=data['warranty']
            )
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('web_view'))

        except IntegrityError:
            db.session.rollback()
            flash('SKU давхцаж байна. Өөр SKU оруулна уу!')
            return redirect(url_for('add_item_web'))
        except ValueError:
            flash('Тоо хэмжээ болон үнэ нь зөв тоо байх ёстой!')
            return redirect(url_for('add_item_web'))

    return render_template('add_item.html')

# Засах
@app.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item_web(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        try:
            data = request.form
            item.sku = data['sku']
            item.name = data['name']
            item.quantity = int(data['quantity'])
            item.location = data['location']
            item.brand = data['brand']
            item.model_no = data['model_no']
            item.price = float(data['price'])
            item.warranty = data['warranty']

            if item.quantity < 0 or item.price < 0:
                flash('Тоо хэмжээ болон үнэ нь 0-с бага байж болохгүй!')
                return redirect(url_for('edit_item_web', item_id=item_id))

            db.session.commit()
            return redirect(url_for('web_view'))

        except ValueError:
            flash('Тоо хэмжээ болон үнэ нь зөв тоо байх ёстой!')
            return redirect(url_for('edit_item_web', item_id=item_id))

    return render_template('edit_item.html', item=item)

# Устгах
@app.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item_web(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('web_view'))

if __name__ == '__main__':
    app.run(debug=True)