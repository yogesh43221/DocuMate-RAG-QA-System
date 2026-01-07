from vector_store import clear_collection, get_stats

def main():
    clear_collection()
    stats = get_stats()
    print("MongoDB stats:", stats)

if __name__ == "__main__":
    main()
