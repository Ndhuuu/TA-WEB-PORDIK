-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2023 at 05:19 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_pordik`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_dataadmin`
--

CREATE TABLE `tb_dataadmin` (
  `id` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(25) NOT NULL,
  `tempat_lahir` varchar(20) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `jenis_kelamin` varchar(10) NOT NULL,
  `agama` varchar(10) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `no_telepon` varchar(15) NOT NULL,
  `email` varchar(20) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_dataadmin`
--

INSERT INTO `tb_dataadmin` (`id`, `username`, `password`, `nama`, `tempat_lahir`, `tanggal_lahir`, `jenis_kelamin`, `agama`, `alamat`, `no_telepon`, `email`, `foto`, `role_id`) VALUES
(8, 'admin1', 'pbkdf2:sha256:260000$4hL0mUpj6KahYk9u$ea8c3f269d8c24025c9eb1eef71e53b2311ce3bf1616a62cf532033a3a5b66cf', 'Ferdy Sambo', 'Barru', '1973-02-09', 'Laki-laki', 'Kristen', 'Jakarta Timur, DKI Jakarta', '089652532796', 'sambocs@gmail.com', NULL, 1),
(9, 'admin2', 'pbkdf2:sha256:260000$1kT5XLlYmVW8Ml5y$66c6fa52aaaeab64118605be4b558f38d096bef660102ca162fde719646fd6c5', 'Teddy Minahasa', 'Manado', '1970-11-23', 'Laki-laki', 'Kristen', 'Sulawesi', '0895', 'teddycs@gmail.com', NULL, 1),
(10, 'admin3', 'pbkdf2:sha256:260000$f61hB0NO2wix9Vzy$65b47a2798c32efb085e7f22c4c6669abfc2bf5cd5db19c8646dadc9708310b5', 'Puan Maharani', 'Jakarta', '1973-09-06', 'Perempuan', 'Islam', 'Jakarta', '0895', 'puancs@gmail.com', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tb_datamahasiswa`
--

CREATE TABLE `tb_datamahasiswa` (
  `id` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(25) NOT NULL,
  `tempat_lahir` varchar(15) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `jenis_kelamin` varchar(10) NOT NULL,
  `agama` varchar(10) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `no_telepon` varchar(15) NOT NULL,
  `email` varchar(20) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_datamahasiswa`
--

INSERT INTO `tb_datamahasiswa` (`id`, `username`, `password`, `nama`, `tempat_lahir`, `tanggal_lahir`, `jenis_kelamin`, `agama`, `alamat`, `no_telepon`, `email`, `foto`, `role_id`) VALUES
(1, '212103032', 'pbkdf2:sha256:260000$i1F03SvoktbmDgcu$396fe48dd7aee055ae0fa50a36a9123b67ffc9f57850faafa76165bdf1738b1c', 'Muhammad Randu Diva', 'Sleman', '2001-12-06', 'Laki-laki', 'Islam', 'Sleman', '089652532796', 'ndhu2001@gmail.com', 'static/img/fotoFerdy_Sambo.png', 2),
(2, '212103035', 'pbkdf2:sha256:260000$5SIXFlDM2JZVGdFl$91a40454476c2ffffab1225c0c1b5a2af9ef4c276baebedab5720dd4dc1ec873', 'Rakhmat Mukti Wibowo', 'Kebumen', '1945-12-01', 'Laki-laki', 'Islam', 'Kebumen', '085157780118', 'rakhmatcs@gmail.com', '', 2),
(3, '111111111', 'pbkdf2:sha256:260000$Cm2QdXUZ4s0dxFVw$b76c043fd9f0683177f40dbfa5c973ed63e221845d2fcb34b0df00d9d212bebf', 'Agung Hapsah', 'Solo', '2023-04-27', 'Laki-laki', 'Islam', 'Solo', '0895', 'agungcs@gmail.com', NULL, 2);

-- --------------------------------------------------------

--
-- Table structure for table `tb_role`
--

CREATE TABLE `tb_role` (
  `id` int(11) NOT NULL,
  `nama` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_role`
--

INSERT INTO `tb_role` (`id`, `nama`) VALUES
(1, 'Admin'),
(2, 'Mahasiswa');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_dataadmin`
--
ALTER TABLE `tb_dataadmin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role` (`role_id`);

--
-- Indexes for table `tb_datamahasiswa`
--
ALTER TABLE `tb_datamahasiswa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role_mahasiswa` (`role_id`);

--
-- Indexes for table `tb_role`
--
ALTER TABLE `tb_role`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_dataadmin`
--
ALTER TABLE `tb_dataadmin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `tb_datamahasiswa`
--
ALTER TABLE `tb_datamahasiswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_dataadmin`
--
ALTER TABLE `tb_dataadmin`
  ADD CONSTRAINT `role_admin` FOREIGN KEY (`role_id`) REFERENCES `tb_role` (`id`);

--
-- Constraints for table `tb_datamahasiswa`
--
ALTER TABLE `tb_datamahasiswa`
  ADD CONSTRAINT `role_mahasiswa` FOREIGN KEY (`role_id`) REFERENCES `tb_role` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
