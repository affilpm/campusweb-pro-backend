import { ReactNode } from 'react';
import { AuthProvider } from '@/contexts/auth-context';
import AdminLayoutClient from './admin-layout-client';

interface AdminLayoutProps {
  children: ReactNode;
}

export default function AdminLayout({ children }: AdminLayoutProps) {
  return (
    <AuthProvider>
      <AdminLayoutClient>{children}</AdminLayoutClient>
    </AuthProvider>
  );
}
