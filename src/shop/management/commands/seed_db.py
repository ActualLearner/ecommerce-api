from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = (
        "Seeds the database with initial categories and products, including image URLs."
    )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to seed the database..."))

        # --- Create All Categories ---
        electronics, _ = Category.objects.get_or_create(
            name="Electronics",
            defaults={"description": "Gadgets, devices, and all things electronic."},
        )
        books, _ = Category.objects.get_or_create(
            name="Books",
            defaults={
                "description": "Fiction, non-fiction, and everything in between."
            },
        )
        clothing, _ = Category.objects.get_or_create(
            name="Clothing",
            defaults={"description": "Apparel for all styles and seasons."},
        )
        home_goods, _ = Category.objects.get_or_create(
            name="Home Goods",
            defaults={"description": "Items to furnish and improve your home."},
        )
        sports, _ = Category.objects.get_or_create(
            name="Sports & Outdoors",
            defaults={"description": "Equipment for an active lifestyle."},
        )
        toys, _ = Category.objects.get_or_create(
            name="Toys & Games", defaults={"description": "Fun and games for all ages."}
        )
        self.stdout.write(self.style.SUCCESS("Categories created successfully."))

        # --- Create All Products with Image URLs ---
        products_to_create = [
            # Electronics
            {
                "name": "Wireless Noise-Cancelling Headphones",
                "category": electronics,
                "description": "High-fidelity audio with adaptive noise cancellation.",
                "price": "249.99",
                "stock": 50,
                "image_url": "https://media.istockphoto.com/id/172847218/photo/headphones.webp?a=1&b=1&s=612x612&w=0&k=20&c=T2Hc4EZubyqfw08TLF6myAcvfUja8lhl7XovA9Ccjx4=",
            },
            {
                "name": "4K Ultra HD Smart TV",
                "category": electronics,
                "description": "A 55-inch smart TV with stunning 4K resolution and HDR.",
                "price": "499.99",
                "stock": 25,
                "image_url": "https://media.istockphoto.com/id/1456456830/photo/wide-screen-led-smart-tv-clipping-path.webp?a=1&b=1&s=612x612&w=0&k=20&c=v6G2avl2eCMMm0QGeR3FRCvT_hufp8Z6MHySbPxix74=",
            },
            {
                "name": "Portable Bluetooth Speaker",
                "category": electronics,
                "description": "Waterproof and dustproof speaker with 12-hour battery life.",
                "price": "79.99",
                "stock": 100,
                "image_url": "https://media.istockphoto.com/id/2197063729/photo/portable-wireless-speaker-isolated-on-white-background.webp?a=1&b=1&s=612x612&w=0&k=20&c=mxW9ctKE2GRVGyKzvkzSdDH79wpjYH-bmlDXrkmXiGg=",
            },
            {
                "name": "E-Reader Tablet",
                "category": electronics,
                "description": "A 6-inch glare-free display that reads like real paper, even in direct sunlight.",
                "price": "129.99",
                "stock": 80,
                "image_url": "https://media.istockphoto.com/id/1468285968/photo/portable-e-book-and-stack-of-hardcover-books-on-white-background.webp?a=1&b=1&s=612x612&w=0&k=20&c=pEGZiPLgVetlhpXaPmlul0dVHtSv4p9CtC02xN3MnpE=",
            },
            # Books
            {
                "name": "The Three-Body Problem",
                "category": books,
                "description": "A science fiction masterpiece by Cixin Liu.",
                "price": "15.99",
                "stock": 150,
                "image_url": "https://prodimage.images-bn.com/pimages/9781250254498_p0_v5_s600x595.jpg",
            },
            {
                "name": "Dune",
                "category": books,
                "description": "Frank Herbert's epic science fiction novel set on the desert planet Arrakis.",
                "price": "18.00",
                "stock": 200,
                "image_url": "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1555447414i/44767458.jpg",
            },
            {
                "name": "Sapiens: A Brief History of Humankind",
                "category": books,
                "description": "Yuval Noah Harari's exploration of human history.",
                "price": "22.50",
                "stock": 120,
                "image_url": "https://m.media-amazon.com/images/I/41r9p0w-a2L._SY445_SX342_FMwebp_.jpg",
            },
            # Clothing
            {
                "name": "Organic Cotton T-Shirt",
                "category": clothing,
                "description": "A soft, breathable, and sustainably sourced t-shirt.",
                "price": "25.00",
                "stock": 300,
                "image_url": "https://media.istockphoto.com/id/482949611/photo/blank-white-t-shirt-front-with-clipping-path.webp?a=1&b=1&s=612x612&w=0&k=20&c=xW5QrpcrFqCSvCetK7hPow9dzankuczBjFT6Z5SC8Kc=",
            },
            {
                "name": "All-Weather Hiking Boots",
                "category": clothing,
                "description": "Durable and waterproof boots for any terrain.",
                "price": "140.00",
                "stock": 60,
                "image_url": "https://media.istockphoto.com/id/936395636/photo/high-mountain-sport-shoe.webp?a=1&b=1&s=612x612&w=0&k=20&c=kXCLkzNgl6wfB0osQbFC2WW95IgVSaHaa11rJAhG81o=",
            },
            # Home Goods
            {
                "name": "Smart LED Light Bulb",
                "category": home_goods,
                "description": "A multi-color smart bulb compatible with voice assistants.",
                "price": "19.99",
                "stock": 250,
                "image_url": "https://m.media-amazon.com/images/I/71QzuIq5NSL._AC_SY300_SX300_QL70_FMwebp_.jpg",
            },
            {
                "name": "Espresso Machine",
                "category": home_goods,
                "description": "A semi-automatic espresso machine with a built-in grinder.",
                "price": "599.00",
                "stock": 15,
                "image_url": "https://m.media-amazon.com/images/I/81pyys3loPL._AC_SY300_SX300_QL70_FMwebp_.jpg",
            },
            # Sports & Outdoors
            {
                "name": "Yoga Mat",
                "category": sports,
                "description": "A non-slip, eco-friendly yoga mat for all types of practice.",
                "price": "35.00",
                "stock": 180,
                "image_url": "https://media.istockphoto.com/id/157592469/photo/rolled-out-yoga-mat.webp?a=1&b=1&s=612x612&w=0&k=20&c=tRL2RJ6gnlZV5K_yBIKAy5Z8dvDWgmLmuX4-q2XXEF8=",
            },
            {
                "name": "2-Person Camping Tent",
                "category": sports,
                "description": "A lightweight, waterproof tent perfect for backpacking.",
                "price": "120.00",
                "stock": 40,
                "image_url": "https://media.istockphoto.com/id/155431954/photo/red-and-white-camping-tent-pitched-to-the-ground.webp?a=1&b=1&s=612x612&w=0&k=20&c=3lmjjL0ZmGz16hMmcDEm18Uv8avnUfd6JdlHdl54rho=",
            },
            # Toys & Games
            {
                "name": "Settlers of Catan Board Game",
                "category": toys,
                "description": "The classic strategy board game of trade, build, and settle.",
                "price": "49.00",
                "stock": 90,
                "image_url": "https://m.media-amazon.com/images/I/81zZW70yiYL._AC_SX679_.jpg",
            },
            {
                "name": "LEGO Space Shuttle Discovery",
                "category": toys,
                "description": "A detailed 2,354-piece model of the iconic NASA space shuttle.",
                "price": "199.99",
                "stock": 20,
                "image_url": "https://m.media-amazon.com/images/I/81WHPrsZQTL._AC_SY450_.jpg",
            },
        ]

        # Keep track of how many new products are actually created
        new_products_created = 0
        for product_data in products_to_create:
            _, created = Product.objects.get_or_create(
                name=product_data["name"],
                category=product_data["category"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                    "image": product_data["image_url"],
                },
            )
            if created:
                new_products_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"{new_products_created} new products created.")
        )
        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
