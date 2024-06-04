package br.com.apaschoalon.repositories;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import br.com.apaschoalon.model.Person;


@Repository
public interface PersonRepository extends JpaRepository<Person, Long>{}
