import pandas as pd
import numpy as np
from models.database import mongo

class Analytics:
    """Analytics utility for generating statistics"""
    
    @staticmethod
    def get_dashboard_stats():
        """Generate comprehensive dashboard statistics"""
        
        # Get all data
        users = list(mongo.db.users.find())
        requests = list(mongo.db.aid_requests.find())
        
        # Convert to DataFrames
        users_df = pd.DataFrame(users) if users else pd.DataFrame()
        requests_df = pd.DataFrame(requests) if requests else pd.DataFrame()
        
        stats = {
            'total_users': len(users),
            'total_donors': len(users_df[users_df['role'] == 'donor']) if not users_df.empty else 0,
            'total_beneficiaries': len(users_df[users_df['role'] == 'beneficiary']) if not users_df.empty else 0,
            'total_requests': len(requests),
            'pending_requests': 0,
            'approved_requests': 0,
            'rejected_requests': 0,
            'completed_requests': 0,
            'total_aid_distributed': 0,
            'average_aid_amount': 0,
            'category_breakdown': {},
            'recent_requests': []
        }
        
        if not requests_df.empty:
            # Status breakdown
            stats['pending_requests'] = len(requests_df[requests_df['status'] == 'pending'])
            stats['approved_requests'] = len(requests_df[requests_df['status'] == 'approved'])
            stats['rejected_requests'] = len(requests_df[requests_df['status'] == 'rejected'])
            stats['completed_requests'] = len(requests_df[requests_df['status'] == 'completed'])
            
            # Financial stats (only for approved/completed)
            distributed = requests_df[requests_df['status'].isin(['approved', 'completed'])]
            if not distributed.empty:
                stats['total_aid_distributed'] = float(distributed['amount'].sum())
                stats['average_aid_amount'] = float(distributed['amount'].mean())
            
            # Category breakdown
            category_counts = requests_df.groupby('category')['amount'].agg(['sum', 'count']).to_dict()
            stats['category_breakdown'] = {
                cat: {
                    'total': float(category_counts['sum'][cat]),
                    'count': int(category_counts['count'][cat])
                } for cat in category_counts['sum'].keys()
            }
            
            # Recent requests (last 5)
            stats['recent_requests'] = requests[-5:] if len(requests) > 5 else requests
        
        return stats
    
    @staticmethod
    def get_category_chart_data():
        """Get data for category-wise aid distribution chart"""
        requests = list(mongo.db.aid_requests.find({'status': {'$in': ['approved', 'completed']}}))
        
        if not requests:
            return {'labels': [], 'data': []}
        
        df = pd.DataFrame(requests)
        category_totals = df.groupby('category')['amount'].sum().to_dict()
        
        return {
            'labels': list(category_totals.keys()),
            'data': [float(v) for v in category_totals.values()]
        }
