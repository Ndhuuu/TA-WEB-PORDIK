-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2023 at 03:53 PM
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
  `password` varchar(20) NOT NULL,
  `nama` varchar(25) NOT NULL,
  `tempat_lahir` varchar(20) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `jenis_kelamin` varchar(10) NOT NULL,
  `agama` varchar(10) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `no_telepon` varchar(15) NOT NULL,
  `email` varchar(20) NOT NULL,
  `foto` longblob DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_dataadmin`
--

INSERT INTO `tb_dataadmin` (`id`, `username`, `password`, `nama`, `tempat_lahir`, `tanggal_lahir`, `jenis_kelamin`, `agama`, `alamat`, `no_telepon`, `email`, `foto`, `role_id`) VALUES
(1, 'admin1', 'admin', 'Ferdy Sambo', 'Barru', '1973-02-09', 'Laki-Laki', 'Kristen', 'Jakarta', '089612345', 'sambocs@gmail.com', NULL, 1),
(2, 'admin2', 'admin', 'Teddy Minahasa', 'Manado', '1970-11-23', 'Laki-Laki', 'Kristen', 'Sulawesi', '0896678910', 'teddycs@gmail.com', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tb_datamahasiswa`
--

CREATE TABLE `tb_datamahasiswa` (
  `id` int(11) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `nama` varchar(25) NOT NULL,
  `tempat_lahir` varchar(15) NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `jenis_kelamin` varchar(10) NOT NULL,
  `agama` varchar(10) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `no_telepon` varchar(15) NOT NULL,
  `email` varchar(20) NOT NULL,
  `foto` longblob DEFAULT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_datamahasiswa`
--

INSERT INTO `tb_datamahasiswa` (`id`, `username`, `password`, `nama`, `tempat_lahir`, `tanggal_lahir`, `jenis_kelamin`, `agama`, `alamat`, `no_telepon`, `email`, `foto`, `role_id`) VALUES
(1, '212103032', 'mahasiswa', 'Muhammad Randu Diva', 'Sleman', '2001-12-06', 'Laki-Laki', 'Islam', 'Sleman', '089652532796', 'ndhu2001@gmail.com', NULL, 2),
(2, '212103035', 'mahasiswa', 'Rakhmat Mukti Wibowo', 'Kebumen', '1945-12-01', 'Laki-Laki', 'Islam', 'Kebumen', '085157780118', 'rakhmatcs@gmail.com', NULL, 2);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tb_datamahasiswa`
--
ALTER TABLE `tb_datamahasiswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
