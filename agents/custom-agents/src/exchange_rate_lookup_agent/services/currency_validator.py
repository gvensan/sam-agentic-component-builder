"""
Currency Validator for input validation
"""

import re
import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class CurrencyValidator:
    """Validator for currency codes and amounts"""
    
    # Major currency codes (ISO 4217)
    MAJOR_CURRENCIES = {
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'CAD': 'Canadian Dollar',
        'AUD': 'Australian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'INR': 'Indian Rupee',
        'BRL': 'Brazilian Real',
        'MXN': 'Mexican Peso',
        'KRW': 'South Korean Won',
        'SGD': 'Singapore Dollar',
        'NZD': 'New Zealand Dollar',
        'SEK': 'Swedish Krona',
        'NOK': 'Norwegian Krone',
        'DKK': 'Danish Krone',
        'PLN': 'Polish Złoty',
        'CZK': 'Czech Koruna',
        'HUF': 'Hungarian Forint',
        'RUB': 'Russian Ruble',
        'TRY': 'Turkish Lira',
        'ZAR': 'South African Rand',
        'THB': 'Thai Baht',
        'MYR': 'Malaysian Ringgit',
        'IDR': 'Indonesian Rupiah',
        'PHP': 'Philippine Peso',
        'VND': 'Vietnamese Dong',
        'EGP': 'Egyptian Pound',
        'NGN': 'Nigerian Naira',
        'KES': 'Kenyan Shilling',
        'GHS': 'Ghanaian Cedi',
        'UGX': 'Ugandan Shilling',
        'TZS': 'Tanzanian Shilling',
        'ZMW': 'Zambian Kwacha',
        'BWP': 'Botswana Pula',
        'NAD': 'Namibian Dollar',
        'MUR': 'Mauritian Rupee',
        'LKR': 'Sri Lankan Rupee',
        'BDT': 'Bangladeshi Taka',
        'PKR': 'Pakistani Rupee',
        'NPR': 'Nepalese Rupee',
        'MMK': 'Myanmar Kyat',
        'KHR': 'Cambodian Riel',
        'LAK': 'Lao Kip',
        'MNT': 'Mongolian Tögrög',
        'KZT': 'Kazakhstani Tenge',
        'UZS': 'Uzbekistani Som',
        'TJS': 'Tajikistani Somoni',
        'KGS': 'Kyrgyzstani Som',
        'TMT': 'Turkmenistan Manat',
        'AZN': 'Azerbaijani Manat',
        'GEL': 'Georgian Lari',
        'AMD': 'Armenian Dram',
        'BYN': 'Belarusian Ruble',
        'MDL': 'Moldovan Leu',
        'UAH': 'Ukrainian Hryvnia',
        'RSD': 'Serbian Dinar',
        'BGN': 'Bulgarian Lev',
        'HRK': 'Croatian Kuna',
        'RON': 'Romanian Leu',
        'BAM': 'Bosnia-Herzegovina Convertible Mark',
        'ALL': 'Albanian Lek',
        'MKD': 'Macedonian Denar',
        'XCD': 'East Caribbean Dollar',
        'BBD': 'Barbadian Dollar',
        'JMD': 'Jamaican Dollar',
        'TTD': 'Trinidad and Tobago Dollar',
        'BZD': 'Belize Dollar',
        'GTQ': 'Guatemalan Quetzal',
        'HNL': 'Honduran Lempira',
        'NIO': 'Nicaraguan Córdoba',
        'CRC': 'Costa Rican Colón',
        'PAB': 'Panamanian Balboa',
        'PYG': 'Paraguayan Guaraní',
        'UYU': 'Uruguayan Peso',
        'CLP': 'Chilean Peso',
        'ARS': 'Argentine Peso',
        'BOB': 'Bolivian Boliviano',
        'PEN': 'Peruvian Sol',
        'COP': 'Colombian Peso',
        'VEF': 'Venezuelan Bolívar',
        'GYD': 'Guyanese Dollar',
        'SRD': 'Surinamese Dollar',
        'XPF': 'CFP Franc',
        'XAF': 'Central African CFA Franc',
        'XOF': 'West African CFA Franc',
        'CDF': 'Congolese Franc',
        'XAF': 'Central African CFA Franc',
        'XOF': 'West African CFA Franc',
        'MAD': 'Moroccan Dirham',
        'TND': 'Tunisian Dinar',
        'DZD': 'Algerian Dinar',
        'LYD': 'Libyan Dinar',
        'SDG': 'Sudanese Pound',
        'ETB': 'Ethiopian Birr',
        'SOS': 'Somali Shilling',
        'DJF': 'Djiboutian Franc',
        'KMF': 'Comorian Franc',
        'MGA': 'Malagasy Ariary',
        'BIF': 'Burundian Franc',
        'RWF': 'Rwandan Franc',
        'MWK': 'Malawian Kwacha',
        'SZL': 'Eswatini Lilangeni',
        'LSL': 'Lesotho Loti',
        'NAD': 'Namibian Dollar',
        'BWP': 'Botswana Pula',
        'ZMW': 'Zambian Kwacha',
        'ZWL': 'Zimbabwean Dollar',
        'AOA': 'Angolan Kwanza',
        'STN': 'São Tomé and Príncipe Dobra',
        'CVE': 'Cape Verdean Escudo',
        'GMD': 'Gambian Dalasi',
        'GNF': 'Guinean Franc',
        'SLL': 'Sierra Leonean Leone',
        'LRD': 'Liberian Dollar',
        'GMD': 'Gambian Dalasi',
        'GNF': 'Guinean Franc',
        'SLL': 'Sierra Leonean Leone',
        'LRD': 'Liberian Dollar',
        'CVE': 'Cape Verdean Escudo',
        'STN': 'São Tomé and Príncipe Dobra',
        'AOA': 'Angolan Kwanza',
        'ZWL': 'Zimbabwean Dollar',
        'ZMW': 'Zambian Kwacha',
        'BWP': 'Botswana Pula',
        'NAD': 'Namibian Dollar',
        'LSL': 'Lesotho Loti',
        'SZL': 'Eswatini Lilangeni',
        'MWK': 'Malawian Kwacha',
        'RWF': 'Rwandan Franc',
        'BIF': 'Burundian Franc',
        'MGA': 'Malagasy Ariary',
        'KMF': 'Comorian Franc',
        'DJF': 'Djiboutian Franc',
        'SOS': 'Somali Shilling',
        'ETB': 'Ethiopian Birr',
        'SDG': 'Sudanese Pound',
        'LYD': 'Libyan Dinar',
        'DZD': 'Algerian Dinar',
        'TND': 'Tunisian Dinar',
        'MAD': 'Moroccan Dirham',
        'XOF': 'West African CFA Franc',
        'XAF': 'Central African CFA Franc',
        'CDF': 'Congolese Franc',
        'XOF': 'West African CFA Franc',
        'XAF': 'Central African CFA Franc',
        'XPF': 'CFP Franc',
        'SRD': 'Surinamese Dollar',
        'GYD': 'Guyanese Dollar',
        'VEF': 'Venezuelan Bolívar',
        'COP': 'Colombian Peso',
        'PEN': 'Peruvian Sol',
        'BOB': 'Bolivian Boliviano',
        'ARS': 'Argentine Peso',
        'CLP': 'Chilean Peso',
        'UYU': 'Uruguayan Peso',
        'PYG': 'Paraguayan Guaraní',
        'PAB': 'Panamanian Balboa',
        'CRC': 'Costa Rican Colón',
        'NIO': 'Nicaraguan Córdoba',
        'HNL': 'Honduran Lempira',
        'GTQ': 'Guatemalan Quetzal',
        'BZD': 'Belize Dollar',
        'TTD': 'Trinidad and Tobago Dollar',
        'JMD': 'Jamaican Dollar',
        'BBD': 'Barbadian Dollar',
        'XCD': 'East Caribbean Dollar',
        'MKD': 'Macedonian Denar',
        'ALL': 'Albanian Lek',
        'BAM': 'Bosnia-Herzegovina Convertible Mark',
        'RON': 'Romanian Leu',
        'HRK': 'Croatian Kuna',
        'BGN': 'Bulgarian Lev',
        'RSD': 'Serbian Dinar',
        'UAH': 'Ukrainian Hryvnia',
        'MDL': 'Moldovan Leu',
        'BYN': 'Belarusian Ruble',
        'AMD': 'Armenian Dram',
        'GEL': 'Georgian Lari',
        'AZN': 'Azerbaijani Manat',
        'TMT': 'Turkmenistan Manat',
        'KGS': 'Kyrgyzstani Som',
        'TJS': 'Tajikistani Somoni',
        'UZS': 'Uzbekistani Som',
        'KZT': 'Kazakhstani Tenge',
        'MNT': 'Mongolian Tögrög',
        'LAK': 'Lao Kip',
        'KHR': 'Cambodian Riel',
        'MMK': 'Myanmar Kyat',
        'NPR': 'Nepalese Rupee',
        'PKR': 'Pakistani Rupee',
        'BDT': 'Bangladeshi Taka',
        'LKR': 'Sri Lankan Rupee',
        'MUR': 'Mauritian Rupee',
        'NAD': 'Namibian Dollar',
        'BWP': 'Botswana Pula',
        'ZMW': 'Zambian Kwacha',
        'TZS': 'Tanzanian Shilling',
        'UGX': 'Ugandan Shilling',
        'GHS': 'Ghanaian Cedi',
        'KES': 'Kenyan Shilling',
        'NGN': 'Nigerian Naira',
        'EGP': 'Egyptian Pound',
        'VND': 'Vietnamese Dong',
        'PHP': 'Philippine Peso',
        'IDR': 'Indonesian Rupiah',
        'MYR': 'Malaysian Ringgit',
        'THB': 'Thai Baht',
        'ZAR': 'South African Rand',
        'TRY': 'Turkish Lira',
        'RUB': 'Russian Ruble',
        'HUF': 'Hungarian Forint',
        'CZK': 'Czech Koruna',
        'PLN': 'Polish Złoty',
        'DKK': 'Danish Krone',
        'NOK': 'Norwegian Krone',
        'SEK': 'Swedish Krona',
        'NZD': 'New Zealand Dollar',
        'SGD': 'Singapore Dollar',
        'KRW': 'South Korean Won',
        'MXN': 'Mexican Peso',
        'BRL': 'Brazilian Real',
        'INR': 'Indian Rupee',
        'CNY': 'Chinese Yuan',
        'CHF': 'Swiss Franc',
        'AUD': 'Australian Dollar',
        'CAD': 'Canadian Dollar',
        'JPY': 'Japanese Yen',
        'GBP': 'British Pound',
        'EUR': 'Euro',
        'USD': 'US Dollar'
    }
    
    @classmethod
    def validate_currency_code(cls, currency_code: str) -> Tuple[bool, str]:
        """
        Validate a currency code
        
        Args:
            currency_code: Currency code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not currency_code:
            return False, "Currency code cannot be empty"
            
        # Convert to uppercase and remove whitespace
        currency_code = currency_code.strip().upper()
        
        # Check format (3 letters)
        if not re.match(r'^[A-Z]{3}$', currency_code):
            return False, f"Invalid currency code format: {currency_code}. Must be 3 uppercase letters."
            
        # Check if it's a supported currency
        if currency_code not in cls.MAJOR_CURRENCIES:
            return False, f"Unsupported currency code: {currency_code}. Please use a supported ISO 4217 currency code."
            
        return True, ""
        
    @classmethod
    def validate_amount(cls, amount: Any) -> Tuple[bool, str]:
        """
        Validate an amount for currency conversion
        
        Args:
            amount: Amount to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount is None:
            return False, "Amount cannot be null"
            
        try:
            # Convert to float
            amount_float = float(amount)
            
            # Check if it's a number
            if not isinstance(amount_float, (int, float)):
                return False, "Amount must be a number"
                
            # Check if it's positive
            if amount_float < 0:
                return False, "Amount must be positive"
                
            # Check if it's not too large (prevent overflow)
            if amount_float > 1e12:  # 1 trillion
                return False, "Amount is too large (maximum: 1 trillion)"
                
            # Check if it's not too small
            if amount_float < 1e-6:  # 0.000001
                return False, "Amount is too small (minimum: 0.000001)"
                
            return True, ""
            
        except (ValueError, TypeError):
            return False, f"Invalid amount format: {amount}. Must be a valid number."
            
    @classmethod
    def get_currency_name(cls, currency_code: str) -> str:
        """
        Get the full name of a currency code
        
        Args:
            currency_code: Currency code
            
        Returns:
            Currency name or "Unknown" if not found
        """
        return cls.MAJOR_CURRENCIES.get(currency_code.upper(), "Unknown")
        
    @classmethod
    def get_supported_currencies(cls) -> Dict[str, str]:
        """
        Get all supported currencies
        
        Returns:
            Dict of currency codes to names
        """
        return cls.MAJOR_CURRENCIES.copy()
        
    @classmethod
    def search_currencies(cls, query: str) -> List[Tuple[str, str]]:
        """
        Search for currencies by name or code
        
        Args:
            query: Search query
            
        Returns:
            List of (code, name) tuples matching the query
        """
        query = query.lower().strip()
        results = []
        
        for code, name in cls.MAJOR_CURRENCIES.items():
            if (query in code.lower() or 
                query in name.lower() or
                any(word in name.lower() for word in query.split())):
                results.append((code, name))
                
        return results
