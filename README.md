# TechX - Tech Products E-Commerce Platform

A modern Django-based e-commerce platform specializing in tech products with an intuitive shopping experience, product management, and content publishing capabilities.

##  Features

- **Product Catalog**
  - Browse and search tech products by category
  - Detailed product pages with specifications
  - Multiple product variants (colors, configurations, SKUs)
  - Product filtering and pagination

- **Shopping Cart**
  - Add/remove items from cart
  - Adjust quantities
  - Cart persistence

- **News & Articles**
  - Publish tech news and articles
  - Track article views
  - Support for featured images
  - Article slugs for SEO-friendly URLs

- **Admin Dashboard**
  - Manage products, variants, and specifications
  - Manage categories
  - Publish and manage articles
  - User and content management

- **Responsive Design**
  - Mobile-friendly interface
  - Professional UI with base template system

##  Technology Stack

- **Backend**: Django 6.0.7
- **Database**: SQLite (db.sqlite3)
- **Image Handling**: Pillow 12.3.0
- **Server**: ASGI/WSGI compatible
- **Python**: 3.x

### Dependencies
```
Django==6.0.7
Pillow==12.3.0
asgiref==3.12.1
sqlparse==0.5.5
tzdata==2026.3
```

##  Project Structure

```
finale/
├── techx_project/          # Main Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py            # Root URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── techx/                 # Main app (categories, products, specs)
│   ├── models.py          # Category, Product, ProductVariant, ProductSpecification
│   ├── views.py           # Homepage and contact views
│   ├── admin.py           # Admin interface setup
│   └── urls.py            # App-specific URL routing
│
├── products/              # Product management app
│   ├── models.py          # Product-related models
│   ├── views.py           # Product list and detail views
│   ├── urls.py            # Product URL routing
│   └── templates/products/
│       ├── products.html        # Product listing page
│       └── product_detail.html  # Product detail page
│
├── news/                  # News and articles app
│   ├── models.py          # Article model
│   ├── views.py           # Article views
│   ├── urls.py            # News URL routing
│   └── templates/news/
│       ├── news.html            # News listing page
│       └── news_detail.html     # Article detail page
│
├── cart/                  # Shopping cart app
│   ├── models.py          # Cart-related models
│   ├── views.py           # Cart views
│   ├── cart.py            # Cart logic/utilities
│   └── templates/cart/
│       └── cart_detail.html     # Cart page
│
├── templates/             # Project-wide templates
│   ├── base.html          # Base template for all pages
│   └── 404.html           # 404 error page
│
├── media/                 # User-uploaded files
│   ├── products/          # Product images
│   └── news/              # Article images
│
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

##  Database Models

### Category
- Stores product categories with slug-based URLs
- Related to: Product (one-to-many)

### Product
- Core product model with name, brand, description
- Features: slug generation, active status
- Related to: Category (ForeignKey), ProductVariant (one-to-many), ProductSpecification (one-to-many)
- Helper: `default_variant` property to get featured variant

### ProductVariant
- Represents product variations (colors, specs, configurations)
- Fields: SKU, color name, specification options, price, stock, image
- Unique constraint: product + color_name + spec_option
- Features: one variant per product marked as default

### ProductSpecification
- Technical specifications for products
- Fields: key (e.g., "Connectivity", "Battery"), value (e.g., "Bluetooth 5.1")
- Unique constraint: product + key

### Article (News)
- Blog/news article model
- Fields: title, slug, summary, content, featured image, author, view count, published status
- Auto-timestamps: created_at, updated_at
- Vietnamese field labels
- Features: auto slug generation, view tracking

##  Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps

1. **Clone/Navigate to the project**
   ```bash
   cd finale
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations** (if needed)
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files** (for production)
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://localhost:8000`

##  Usage

### Accessing the Admin Interface
1. Navigate to `http://localhost:8000/admin`
2. Login with your superuser credentials
3. Manage categories, products, variants, articles, and users

### Adding Products
1. Go to Admin → Techx → Categories (create if needed)
2. Go to Admin → Techx → Products
3. Create a new product, assign a category
4. Add ProductVariants (colors/specs) with images and pricing
5. Add ProductSpecifications (technical details)

### Publishing Articles
1. Go to Admin → News → Articles
2. Create new article with title, content, and featured image
3. Set "Is Published" to make it visible
4. Articles automatically generate SEO-friendly slugs

### Shopping Features
- Users can browse products on `/products/`
- Filter by category or search by keyword
- View product details and specifications
- Add items to cart via `/cart/`

##  Configuration

### Important Settings in `techx_project/settings.py`
- `DEBUG = False` - Set to `True` for development
- `ALLOWED_HOSTS` - Add your domain in production
- `SECRET_KEY` - Change in production (currently not secure)
- `INSTALLED_APPS` - Register all Django apps
- `MEDIA_ROOT` - Where uploaded files are stored
- `MEDIA_URL` - Public URL for media files

### Security Notes
- ⚠️ Change `SECRET_KEY` before deploying to production
- ⚠️ Set `DEBUG = False` in production
- ⚠️ Use environment variables for sensitive data
- ⚠️ Configure proper `ALLOWED_HOSTS` for your domain

##  Development Tips

### Useful Django Management Commands
```bash
# Create a new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Shell for interactive database access
python manage.py shell

# Run tests
python manage.py test
```

### Admin Customization
- Edit `admin.py` in each app to customize the admin interface
- Use `list_display`, `search_fields`, `list_filter` for better UX

##  Contributing

When contributing to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Update documentation
5. Submit a pull request

##  License

This project is open source. Please check for specific license information.

##  Support

For issues or questions, please create an issue in the repository.

---

**Last Updated**: August 2026
