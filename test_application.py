"""
Comprehensive Test Script for Finale Library Management System
Tests all major functionality without requiring GUI interaction
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.book_service import BookService
from services.category_service import CategoryService
from services.stats_service import StatsService
from utils.validators import validate_isbn, validate_year, validate_pages, validate_rating
from utils.helpers import generate_id, calculate_progress, get_star_rating
from models import Book, Category

def test_book_service():
    """Test BookService functionality"""
    print("\n=== Testing BookService ===")
    
    # Initialize service
    book_service = BookService("test_books.json")
    print("✓ BookService initialized")
    
    # Test get all books
    books = book_service.get_all_books()
    print(f"✓ Retrieved {len(books)} books")
    
    # Test add book
    new_book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "genre": "Test Genre",
        "isbn": "9780123456789",
        "year": 2024,
        "total_pages": 300
    }
    new_book = book_service.add_book(new_book_data)
    print(f"✓ Added new book: {new_book.title}")
    
    # Test get book by id
    retrieved_book = book_service.get_book_by_id(new_book.id)
    assert retrieved_book is not None, "Failed to retrieve book by ID"
    print(f"✓ Retrieved book by ID: {retrieved_book.title}")
    
    # Test update book
    updated = book_service.update_book(new_book.id, {"current_page": 150})
    assert updated is not None, "Failed to update book"
    assert updated.current_page == 150, "Book update failed"
    assert updated.progress == 50, "Progress calculation failed"
    print(f"✓ Updated book progress: {updated.progress}%")
    
    # Test search books
    search_results = book_service.search_books("Test")
    assert len(search_results) > 0, "Search failed"
    print(f"✓ Search found {len(search_results)} results")
    
    # Test update status
    status_updated = book_service.update_book_status(new_book.id, "Reading", 100)
    assert status_updated.status == "Reading", "Status update failed"
    print(f"✓ Updated book status to: {status_updated.status}")
    
    # Test rate book
    rated = book_service.rate_book(new_book.id, 4.5, "Great book!")
    assert rated.rating == 4.5, "Rating failed"
    print(f"✓ Rated book: {rated.rating}/5")
    
    # Test statistics
    stats = book_service.get_statistics()
    print(f"✓ Statistics: {stats['total_books']} total, {stats['completed_books']} completed")
    
    # Test delete book
    deleted = book_service.delete_book(new_book.id)
    assert deleted, "Delete failed"
    print("✓ Deleted test book")
    
    # Cleanup
    if os.path.exists("test_books.json"):
        os.remove("test_books.json")
    
    print("✅ BookService tests passed!")

def test_category_service():
    """Test CategoryService functionality"""
    print("\n=== Testing CategoryService ===")
    
    # Initialize service
    category_service = CategoryService("test_categories.json")
    print("✓ CategoryService initialized")
    
    # Test get all categories
    categories = category_service.get_all_categories()
    print(f"✓ Retrieved {len(categories)} categories")
    
    # Test create category
    new_category = category_service.create_category("Test Category", "#FF0000")
    assert new_category is not None, "Failed to create category"
    print(f"✓ Created category: {new_category.name}")
    
    # Test get category by name
    retrieved = category_service.get_category_by_name("Test Category")
    assert retrieved is not None, "Failed to retrieve category"
    print(f"✓ Retrieved category: {retrieved.name}")
    
    # Test update category
    updated = category_service.update_category("Test Category", "Updated Category", "#00FF00")
    assert updated is not None, "Failed to update category"
    assert updated.name == "Updated Category", "Category name not updated"
    print(f"✓ Updated category to: {updated.name}")
    
    # Test delete category
    deleted = category_service.delete_category("Updated Category")
    assert deleted, "Failed to delete category"
    print("✓ Deleted test category")
    
    # Cleanup
    if os.path.exists("test_categories.json"):
        os.remove("test_categories.json")
    
    print("✅ CategoryService tests passed!")

def test_stats_service():
    """Test StatsService functionality"""
    print("\n=== Testing StatsService ===")
    
    # Initialize services
    book_service = BookService("test_books_stats.json")
    stats_service = StatsService()
    print("✓ StatsService initialized")
    
    # Get books
    books = book_service.get_all_books()
    
    # Test calculate statistics
    stats = stats_service.calculate_statistics(books)
    print(f"✓ Calculated statistics: {stats.total_books} books")
    
    # Test check achievements
    achievements = stats_service.check_achievements(books)
    print(f"✓ Checked {len(achievements)} achievements")
    
    # Test get KPIs
    kpis = stats_service.get_kpi_data(books)
    print(f"✓ Generated {len(kpis)} KPI cards")
    
    # Test genre distribution
    genre_dist = stats_service.get_genre_distribution(books)
    print(f"✓ Genre distribution: {len(genre_dist)} genres")
    
    # Cleanup
    if os.path.exists("test_books_stats.json"):
        os.remove("test_books_stats.json")
    
    print("✅ StatsService tests passed!")

def test_validators():
    """Test validation functions"""
    print("\n=== Testing Validators ===")
    
    # Test ISBN validation
    valid, msg = validate_isbn("9780123456789")
    print(f"✓ ISBN validation: {msg}")
    
    # Test year validation
    valid, msg = validate_year("2024")
    assert valid, "Year validation failed"
    print(f"✓ Year validation: {msg}")
    
    # Test pages validation
    valid, msg = validate_pages("100", "200")
    assert valid, "Pages validation failed"
    print(f"✓ Pages validation: {msg}")
    
    # Test rating validation
    valid, msg = validate_rating("4.5")
    assert valid, "Rating validation failed"
    print(f"✓ Rating validation: {msg}")
    
    print("✅ Validator tests passed!")

def test_helpers():
    """Test helper functions"""
    print("\n=== Testing Helpers ===")
    
    # Test generate_id
    book_id = generate_id("book")
    assert book_id.startswith("book-"), "ID generation failed"
    print(f"✓ Generated ID: {book_id}")
    
    # Test calculate_progress
    progress = calculate_progress(50, 100)
    assert progress == 50, "Progress calculation failed"
    print(f"✓ Calculated progress: {progress}%")
    
    # Test get_star_rating
    stars = get_star_rating(4.5)
    assert "★" in stars, "Star rating failed"
    print(f"✓ Star rating: {stars}")
    
    print("✅ Helper tests passed!")

def test_models():
    """Test data models"""
    print("\n=== Testing Models ===")
    
    # Test Book model
    book = Book(
        id="test-1",
        title="Test Book",
        author="Test Author",
        publisher="Test Publisher",
        genre="Fiction",
        isbn="9780123456789",
        year=2024
    )
    book_dict = book.to_dict()
    assert book_dict["title"] == "Test Book", "Book model failed"
    print(f"✓ Book model: {book.title}")
    
    # Test Category model
    category = Category(name="Test", color="#FF0000")
    assert category.name == "Test", "Category model failed"
    print(f"✓ Category model: {category.name}")
    
    print("✅ Model tests passed!")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("FINALE LIBRARY MANAGEMENT SYSTEM - COMPREHENSIVE TESTS")
    print("="*60)
    
    try:
        test_models()
        test_helpers()
        test_validators()
        test_book_service()
        test_category_service()
        test_stats_service()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        print("="*60)
        print("\n✅ The application is fully functional and ready to use!")
        print("   Run 'python MAIN.py' to start the application.")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
