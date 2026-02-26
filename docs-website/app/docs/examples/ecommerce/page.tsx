import { DocPage, CodeBlock, Callout } from '@/components/DocPage';

export default function EcommerceExamplePage() {
  return (
    <DocPage title="E-commerce API" description="A complete e-commerce API with products, carts, orders, and JWT auth.">

      <h2>Generate the Project</h2>
      <CodeBlock
        language="bash"
        code={`shanks new shop-api
cd shop-api
shanks create products --crud
shanks create orders --crud
shanks create auth --simple
sorm db push
shanks run`}
      />

      <h2>Product Model</h2>
      <CodeBlock
        filename="entity/product.py"
        code={`from django.db import models

class Product(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.IntegerField(default=0)
    category    = models.CharField(max_length=100, blank=True)
    image_url   = models.URLField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'entity'`}
      />

      <h2>Products Route</h2>
      <CodeBlock
        filename="internal/routes/products.py"
        code={`from shanks import App, Response
from entity.product import Product

app = App()

@app.get('api/products')
def list_products(req):
    category = req.query.get('category')
    products = Product.find_many(category=category) if category else Product.find_many()
    return {'products': [{'id': p.id, 'name': p.name, 'price': str(p.price)} for p in products]}

@app.get('api/products/<product_id>')
def get_product(req, product_id):
    product = Product.find_unique(id=product_id)
    if not product:
        return Response().status_code(404).json({'error': 'Not found'})
    return {'product': {'id': product.id, 'name': product.name, 'price': str(product.price), 'stock': product.stock}}

router = app`}
      />

      <h2>API Endpoints</h2>
      <CodeBlock
        language="text"
        code={`GET  /api/products              List products (filter by ?category=)
GET  /api/products/<id>         Product detail
POST /api/products              Create (admin only)
PUT  /api/products/<id>         Update (admin only)

GET  /api/orders                My orders (JWT required)
POST /api/orders                Place an order (JWT required)
GET  /api/orders/<id>           Order detail`}
      />

      <Callout type="info">
        Products are cached automatically — your product listing page will be 10× faster after the first request.
      </Callout>
    </DocPage>
  );
}
