import './styles.css';

export const metadata = { title: 'CyberOS — Global Cybersecurity Intelligence', description: 'Cybersecurity intelligence and security posture platform' };

export default function RootLayout({ children }) {
  return <html lang="en"><body>{children}</body></html>;
}
