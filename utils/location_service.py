import math
from django.db.models import Q
from bloodbank.models import BloodBank
from bloodrequests.models import BloodRequest
from bloodstock.models import Stock

class LocationService:
    """Service for handling location-based operations and distance calculations"""
    
    # Approximate coordinates for major Egyptian cities (latitude, longitude)
    CITY_COORDINATES = {
        'Cairo': (30.0444, 31.2357),
        'Alexandria': (31.2001, 29.9187),
        'Giza': (30.0131, 31.2089),
        'Shubra El Kheima': (30.1287, 31.2441),
        'Port Said': (31.2653, 32.3019),
        'Suez': (29.9668, 32.5498),
        'Luxor': (25.6872, 32.6396),
        'Mansoura': (31.0409, 31.3785),
        'El Mahalla El Kubra': (30.9765, 31.1669),
        'Tanta': (30.7865, 31.0004),
        'Asyut': (27.1809, 31.1837),
        'Ismailia': (30.5965, 32.2715),
        'Fayyum': (29.3084, 30.8428),
        'Zagazig': (30.5877, 31.5022),
        'Aswan': (24.0889, 32.8998),
        'Damietta': (31.4165, 31.8133),
        'Damanhur': (31.0341, 30.4682),
        'Minya': (28.0871, 30.7618),
        'Beni Suef': (29.0661, 31.0994),
        'Qena': (26.1551, 32.7160),
        'Sohag': (26.5569, 31.6948),
        'Hurghada': (27.2574, 33.8129),
        'Sharm El Sheikh': (27.9158, 34.3300),
        'Marsa Matruh': (31.3543, 27.2373),
        'Arish': (31.1313, 33.7989),
        'Mallawi': (27.7311, 30.8418),
        'Bilbays': (30.4204, 31.5658),
        'Mit Ghamr': (30.7119, 31.2596),
        'Kafr El Sheikh': (31.1107, 30.9388),
        'Quesna': (30.5647, 31.1158)
    }
    
    @staticmethod
    def get_city_coordinates(city_name):
        """Get coordinates for a city"""
        return LocationService.CITY_COORDINATES.get(city_name)
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees) using Haversine formula
        Returns distance in kilometers
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r
    
    @staticmethod
    def get_distance_between_cities(city1, city2):
        """Get distance between two cities in kilometers"""
        coords1 = LocationService.get_city_coordinates(city1)
        coords2 = LocationService.get_city_coordinates(city2)
        
        if not coords1 or not coords2:
            return None
        
        return LocationService.calculate_distance(
            coords1[0], coords1[1], coords2[0], coords2[1]
        )
    
    @staticmethod
    def find_nearby_blood_banks(city_name, max_distance_km=50):
        """
        Find blood banks within a specified distance from a city
        Returns list of (blood_bank, distance) tuples sorted by distance
        """
        city_coords = LocationService.get_city_coordinates(city_name)
        if not city_coords:
            return []
        
        nearby_banks = []
        blood_banks = BloodBank.objects.all()
        
        for bank in blood_banks:
            bank_coords = LocationService.get_city_coordinates(bank.city.name)
            if bank_coords:
                distance = LocationService.calculate_distance(
                    city_coords[0], city_coords[1],
                    bank_coords[0], bank_coords[1]
                )
                
                if distance <= max_distance_km:
                    nearby_banks.append((bank, distance))
        
        # Sort by distance
        nearby_banks.sort(key=lambda x: x[1])
        return nearby_banks
    
    @staticmethod
    def find_blood_banks_for_request(blood_request, max_distance_km=100):
        """
        Find blood banks that can fulfill a blood request, sorted by distance and stock availability
        Returns list of dictionaries with bank info, distance, and available stock
        """
        hospital_city = blood_request.hospital.user.city.name
        hospital_coords = LocationService.get_city_coordinates(hospital_city)
        
        if not hospital_coords:
            return []
        
        # Find blood banks with matching stock
        available_banks = []
        stocks = Stock.objects.filter(
            blood_type=blood_request.blood_type,
            quantity__gte=blood_request.quantity
        ).select_related('blood_bank', 'blood_bank__city')
        
        for stock in stocks:
            bank = stock.blood_bank
            bank_coords = LocationService.get_city_coordinates(bank.city.name)
            
            if bank_coords:
                distance = LocationService.calculate_distance(
                    hospital_coords[0], hospital_coords[1],
                    bank_coords[0], bank_coords[1]
                )
                
                if distance <= max_distance_km:
                    available_banks.append({
                        'bank': bank,
                        'distance_km': round(distance, 2),
                        'available_stock': stock.quantity,
                        'stock_id': stock.id,
                        'city': bank.city.name
                    })
        
        # Sort by distance first, then by available stock (descending)
        available_banks.sort(key=lambda x: (x['distance_km'], -x['available_stock']))
        return available_banks
    
    @staticmethod
    def get_blood_bank_coverage_area(blood_bank, max_distance_km=50):
        """
        Get all cities within coverage area of a blood bank
        Returns list of (city_name, distance) tuples
        """
        bank_coords = LocationService.get_city_coordinates(blood_bank.city.name)
        if not bank_coords:
            return []
        
        coverage_cities = []
        
        for city_name, city_coords in LocationService.CITY_COORDINATES.items():
            distance = LocationService.calculate_distance(
                bank_coords[0], bank_coords[1],
                city_coords[0], city_coords[1]
            )
            
            if distance <= max_distance_km:
                coverage_cities.append((city_name, round(distance, 2)))
        
        # Sort by distance
        coverage_cities.sort(key=lambda x: x[1])
        return coverage_cities
    
    @staticmethod
    def optimize_blood_request_matching(blood_requests, priority_weight=0.7, distance_weight=0.3):
        """
        Optimize blood request matching considering both priority and distance
        Returns optimized matching suggestions
        """
        if not blood_requests:
            return []
        
        matching_results = []
        
        for request in blood_requests:
            # Get priority score (high=3, medium=2, low=1)
            priority_scores = {'high': 3, 'medium': 2, 'low': 1}
            priority_score = priority_scores.get(request.priority, 1)
            
            # Find available blood banks
            available_banks = LocationService.find_blood_banks_for_request(request)
            
            for bank_info in available_banks:
                # Calculate distance score (inverse of distance, normalized)
                max_distance = 100  # km
                distance_score = max(0, (max_distance - bank_info['distance_km']) / max_distance)
                
                # Calculate combined score
                combined_score = (priority_score * priority_weight) + (distance_score * distance_weight)
                
                matching_results.append({
                    'request': request,
                    'bank_info': bank_info,
                    'priority_score': priority_score,
                    'distance_score': distance_score,
                    'combined_score': combined_score,
                    'recommendation': LocationService._get_recommendation_text(
                        request, bank_info, combined_score
                    )
                })
        
        # Sort by combined score (highest first)
        matching_results.sort(key=lambda x: x['combined_score'], reverse=True)
        return matching_results
    
    @staticmethod
    def _get_recommendation_text(request, bank_info, score):
        """Generate recommendation text based on matching score"""
        if score >= 2.5:
            return f"HIGHLY RECOMMENDED: {bank_info['bank'].name} is {bank_info['distance_km']}km away with {bank_info['available_stock']}ml available"
        elif score >= 2.0:
            return f"RECOMMENDED: {bank_info['bank'].name} is {bank_info['distance_km']}km away with {bank_info['available_stock']}ml available"
        elif score >= 1.5:
            return f"CONSIDER: {bank_info['bank'].name} is {bank_info['distance_km']}km away with {bank_info['available_stock']}ml available"
        else:
            return f"LAST RESORT: {bank_info['bank'].name} is {bank_info['distance_km']}km away with {bank_info['available_stock']}ml available"
    
    @staticmethod
    def get_location_analytics():
        """Get analytics about location-based distribution"""
        analytics = {
            'total_cities': len(LocationService.CITY_COORDINATES),
            'cities_with_banks': BloodBank.objects.values('city__name').distinct().count(),
            'average_coverage_per_bank': 0,
            'coverage_gaps': []
        }
        
        # Calculate coverage gaps (cities without nearby blood banks)
        cities_without_coverage = []
        for city_name in LocationService.CITY_COORDINATES.keys():
            nearby_banks = LocationService.find_nearby_blood_banks(city_name, max_distance_km=30)
            if not nearby_banks:
                cities_without_coverage.append(city_name)
        
        analytics['coverage_gaps'] = cities_without_coverage
        analytics['cities_without_nearby_banks'] = len(cities_without_coverage)
        
        return analytics
